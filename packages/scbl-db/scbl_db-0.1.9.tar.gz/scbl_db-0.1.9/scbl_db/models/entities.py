from functools import cached_property
from os import environ
from pathlib import Path
from re import fullmatch

from email_validator import validate_email
from sqlalchemy import ForeignKey, UniqueConstraint, inspect
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from urllib3 import request

from ..bases import Entity
from ..custom_types import (
    SamplesheetString,
    StrippedString,
    stripped_str,
    unique_stripped_str,
)
from ..utils import get_format_string_vars

__all__ = ['Institution', 'Lab', 'Person']


class Institution(Entity, kw_only=True):
    __tablename__ = 'institution'

    # Institution attributes
    email_format: Mapped[stripped_str] = mapped_column(repr=False, compare=False)
    ror_id: Mapped[unique_stripped_str | None] = mapped_column(
        default=None, repr=False, compare=False
    )
    name: Mapped[unique_stripped_str] = mapped_column(default=None, index=True)
    short_name: Mapped[stripped_str] = mapped_column(
        default=None, index=True, compare=False
    )
    country: Mapped[str] = mapped_column(StrippedString(length=2), default='US')
    state: Mapped[str | None] = mapped_column(StrippedString(length=2), default=None)
    city: Mapped[stripped_str] = mapped_column(default=None)

    @validates('email_format')
    def validate_email_format(self, key: str, email_format: str) -> str:
        email_format = email_format.strip().lower()

        variables = get_format_string_vars(email_format)

        if not variables:
            raise ValueError(f'No variables found in {key} {email_format}')

        person_columns = set(inspect(Person).columns.keys())
        non_existent_person_columns = variables - person_columns

        if non_existent_person_columns:
            raise ValueError(
                f'The following variables in {email_format} are not members of {person_columns}:\n{non_existent_person_columns}'
            )

        example_values = {var: 'string' for var in variables}
        example_email = email_format.format_map(example_values)

        validate_email(example_email)

        return email_format

    @cached_property
    def _ror_data(self):
        if self.ror_id is None:
            return None

        base_url = 'https://api.ror.org/organizations'
        url = f'{base_url}/{self.ror_id}'
        response = request(method='GET', url=url)

        if response.status != 200:
            raise ValueError(
                f'ROR ID {self.ror_id} not found in database search of {base_url}'
            )

        return response.json()

    def __post_init__(self):
        if self._ror_data is None:
            if not all((self.name, self.short_name, self.country, self.city)):
                raise ValueError(
                    'If ROR ID is not provided, then name, short_name, country, and city must be provided.'
                )
            return

        if self.name is None:
            self.name = self._ror_data['name']

        acronyms = self._ror_data['acronyms']
        aliases = self._ror_data['aliases']
        if self.short_name is None:
            if len(acronyms) > 0:
                self.short_name = acronyms[0]
            elif len(aliases) > 0:
                self.short_name = aliases[0]
            else:
                raise ValueError(
                    'Could not find short name from ROR data. Please provide manually.'
                )

        self.country = self._ror_data['country']['country_code']

        acronyms = self._ror_data['acronyms']
        aliases = self._ror_data['aliases']
        if self.short_name is None:
            if len(acronyms) > 0:
                self.short_name = acronyms[0]
            elif len(aliases) > 0:
                self.short_name = aliases[0]
            else:
                pass

        self.country = self._ror_data['country']['country_code']

        addresses = self._ror_data['addresses']
        if len(addresses) > 0:
            geonames_city_info = addresses[0]['geonames_city']
            self.city = geonames_city_info['city']
            if self.country == 'US':
                state_code = geonames_city_info['geonames_admin1']['code']
                _, self.state = state_code.split('.')
        else:
            raise ValueError(
                f'Could not find city information from ROR for {self.name}. Please enter manually.'
            )


class Person(Entity, kw_only=True):
    __tablename__ = 'person'

    # Person attributes
    first_name: Mapped[stripped_str]
    last_name: Mapped[stripped_str]
    orcid: Mapped[unique_stripped_str | None] = mapped_column(
        default=None, repr=False, compare=False
    )
    email_auto_generated: Mapped[bool] = mapped_column(
        init=False, default=False, repr=False, compare=False
    )
    email: Mapped[unique_stripped_str] = mapped_column(default=None, index=True)

    # Parent foreign keys
    institution_id: Mapped[int] = mapped_column(
        ForeignKey('institution.id'), repr=False, compare=False, default=None
    )

    # Parent models
    institution: Mapped[Institution] = relationship(
        repr=False, compare=False, default=None
    )

    @validates('first_name', 'last_name')
    def format_name(self, key: str, name: str) -> str:
        formatted_split = name.strip().title().split()
        noramlized_inner_whitespace = ' '.join(formatted_split)
        return noramlized_inner_whitespace

    @validates('orcid')
    def validate_orcid(self, key: str, orcid: str | None) -> str | None:
        if orcid is None:
            return orcid

        orcid = orcid.strip()

        orcid_pattern = r'(\d{4})-?(\d{4})-?(\d{4})-?(\d{4}|\d{3}X)'
        if (match_obj := fullmatch(orcid_pattern, string=orcid)) is None:
            raise ValueError(f'ORCID {orcid} does not match pattern {orcid_pattern}')

        digit_groups = match_obj.groups()
        formatted_orcid = '-'.join(digit_groups)

        base_url = 'https://pub.orcid.org'
        url = f'{base_url}/{formatted_orcid}'
        headers = {'Accept': 'application/json'}
        response = request(method='GET', url=url, headers=headers)

        if response.status != 200:
            raise ValueError(
                f'{formatted_orcid} not found in database search of {base_url}'
            )

        return formatted_orcid

    @validates('email')
    def validate_email(self, key: str, email: str | None) -> str | None:
        if email is None:
            return email

        email_info = validate_email(email.lower(), check_deliverability=True)
        return email_info.normalized

    def __post_init__(self):
        if self.email is not None:
            return

        variables = get_format_string_vars(self.institution.email_format)
        var_values = {var: getattr(self, var) for var in variables}

        self.email = self.institution.email_format.format_map(var_values).replace(
            ' ', ''
        )
        self.email_auto_generated = True


class Lab(Entity, kw_only=True):
    __tablename__ = 'lab'

    # Lab attributes
    name: Mapped[stripped_str] = mapped_column(default=None, index=True)
    delivery_dir: Mapped[unique_stripped_str] = mapped_column(default=None, repr=False)
    unix_group: Mapped[stripped_str] = mapped_column(
        init=False, default=None, repr=False, compare=False
    )

    # Parent foreign keys
    institution_id: Mapped[int] = mapped_column(
        ForeignKey('institution.id'), repr=False, compare=False, default=None
    )
    pi_id: Mapped[int] = mapped_column(
        ForeignKey('person.id'), repr=False, compare=False, default=None
    )

    # Parent models
    institution: Mapped[Institution] = relationship(default=None)
    pi: Mapped[Person] = relationship(default=None)

    __table_args__ = (UniqueConstraint('institution_id', 'pi_id', 'name'),)

    @cached_property
    def _delivery_parent_dir(self) -> Path:
        return Path(environ['delivery_parent_dir'])

    @validates('delivery_dir')
    def validate_delivery_dir(self, key: str, delivery_dir: str | None):
        if delivery_dir is None:
            return delivery_dir

        delivery_path = self._delivery_parent_dir / delivery_dir
        if not delivery_path.is_dir():
            raise NotADirectoryError(f'{key} {delivery_path} is not a directory.')

        return str(delivery_path)

    def __post_init__(self):
        if self.name is None:
            self.name = f'{self.pi.first_name} {self.pi.last_name} Lab'

        if self.delivery_dir is not None:
            self.unix_group = Path(self.delivery_dir).group()
            return

        pi = self.pi

        first_name = SamplesheetString().process_bind_param(
            pi.first_name.lower(), dialect=None
        )
        last_name = SamplesheetString().process_bind_param(
            pi.last_name.lower(), dialect=None
        )

        delivery_path = self._delivery_parent_dir / f'{first_name}_{last_name}'
        if not delivery_path.is_dir():
            raise NotADirectoryError(
                f'Delivery directory {delivery_path} does not exist.'
            )

        self.delivery_dir = str(delivery_path)
        self.unix_group = delivery_path.group()
