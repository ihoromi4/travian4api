import bs4


def parse_tradeoffice(soup: bs4.BeautifulSoup) -> int:
    div = soup.find('div', {'id': 'build'})
    if not div:
        return -1
    div = div.find('div', {'id': 'descriptionAndInfo'})
    if not div:
        return -2
    table = div.find('table')
    if not table:
        return -3
    span = table.find('span', {'class': 'number'})
    if not span:
        return -4
    carry = int(span.text)
    return carry
