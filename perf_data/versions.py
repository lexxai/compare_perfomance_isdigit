import re


def version_1(string: str) -> str:
    digits = []
    for char in string:
        if char.isdigit():
            digits.append(char)
    return "".join(digits)


def version_2(string: str) -> str:
    return "".join([char for char in string if char.isdigit()])


def version_3(string: str) -> str:
    return "".join(filter(str.isdigit, string))


def version_4(string: str) -> str:
    return "".join(re.findall(r"\d+", string))


REGEX = re.compile(r"\d+")


def version_5(string: str) -> str:
    return "".join(re.findall(REGEX, string))


def version_6(string: str) -> str:
    return "".join(REGEX.findall(string))
