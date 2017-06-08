import bs4

from . import base


def parse_alliance_description(soup: bs4.BeautifulSoup) -> dict:
    description = dict()

    div_details = soup.find('div', {'id': 'details'})
    table = div_details.find('table')
    tds = table.find_all('td')

    description['abbreviation'] = tds[0].text
    description['name'] = tds[1].text
    description['range'] = int(tds[2].text)
    description['score'] = int(tds[3].text)
    description['members_count'] = int(tds[4].text)

    # div_memberTitles = soup.find('div', {'id': 'memberTitles'})
    # table = div_memberTitles.find('table')

    return description


def parse_alliance_members(soup: bs4.BeautifulSoup) -> list:
    table = soup.find('table', {'class': 'allianceMembers'})
    rows = table.find_all('tr')
    rows = rows[1:]  # удаляем строку с заголовками
    members = []
    for row in rows:
        member = dict()
        tds = row.find_all('td')
        # counter:
        member['counter'] = int(float(tds[0].text))  # str like 1. -> float 1.0 -> int 1
        # tribe
        # player online:
        img = tds[2].find('img')
        online_classes = img['class']
        online_class = online_classes[0]  # str like 'online<int>'
        online = int(online_class[-1])  # 'online<int>' -> <int>
        member['online'] = online
        # player href:
        a = tds[2].find('a')
        member['href'] = a['href']
        # player uid:
        member['uid'] = base.href_to_uid(a['href'])
        # player name:
        member['name'] = a.text
        # population:
        member['population'] = int(tds[3].text)
        # villages:
        member['villages'] = int(tds[4].text)

        members.append(member)
    return members
