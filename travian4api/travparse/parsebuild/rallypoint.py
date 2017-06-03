import bs4


def parse_table(table: bs4.NavigableString):
    result = {}
    tbodies = table.find_all('tbody')
    imgs = tbodies[0].find_all('img')
    tds_number = tbodies[1].find_all('td')
    for img, td_number in zip(imgs, tds_number):
        try:
            unit_type = int(img['class'][1][1:])
        except ValueError:
            unit_type = img['class'][1][1:]
        number = int(td_number.text.strip())
        result[unit_type] = number
    return result


def parse_troops(soup: bs4.BeautifulSoup):
    troops = {}
    div_data = soup.find('div', {'class': 'data'})

    tables_in_return = div_data.find_all('table', {'class': 'troop_details inReturn'})
    troops['incoming'] = []
    for table in tables_in_return:
        units = parse_table(table)
        troops['incoming'].append(units)
    else:
        pass

    tables_out_raid = div_data.find_all('table', {'class': 'troop_details outRaid'})
    troops['outgoing'] = []
    for table in tables_out_raid:
        units = parse_table(table)
        troops['outgoing'].append(units)
    else:
        pass

    tables_in_village = div_data.find_all('table', {'class': 'troop_details'})
    troops['in_village'] = []
    for table in tables_in_village:
        if len(table['class']) > 1:
            continue
        units = parse_table(table)
        troops['in_village'].append(units)
    else:
        pass

    return troops
