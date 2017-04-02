import re


def get_one_match(pattern, text):
    result = re.findall(pattern, text)
    if len(result) == 0:
        raise ValueError('No matches')
    return result[0]


def href_to_uid(href: str) -> int:
    pattern = r'uid=(\d+)'
    return int(get_one_match(pattern, href))


def href_to_did(href: str) -> int:
    pattern = r'd=(\d+)'
    return int(get_one_match(pattern, href))


def get_time(text: str):
    pattern = r'(\d\d:\d\d)'
    return get_one_match(pattern, text)
