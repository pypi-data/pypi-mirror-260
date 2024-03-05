from re import findall


def get_format_string_vars(string: str) -> set[str]:
    pattern = r'{(\w+)(?:\[\d+\])?}'
    variables = set(findall(pattern, string))

    return variables
