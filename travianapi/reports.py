import re

import bs4

from . import login

'''
Ближайшие цели для реализации:
- Парсинг списка нападений:
    Определение набегов
    Определение украденых ресурсов
    Определение потерь
- Парсинг разведывательных операций:

- Изменение статуса отчетов на "просмотренно"
- Удаление отчетов
'''

report_types = [
    1,      # успешная атака (атака или набег)
    2,      # атака с потерями
    3,      # предположительно: неудачная атака - все войска погибли
    15,     # успешная разведка
    16,     # предположительно: разведка с потерями
    17      # предположительно: неудачная разведка - все погибли
]


class Reports:
    def __init__(self, account):
        self.account = account
        self.login = account.login
        # ---
        html = self.login.server_get('berichte.php')
        soup = bs4.BeautifulSoup(html, 'html5lib')
        button_submit = soup.find('button', {'name': 'del'})
        self.word_delete = button_submit['value']
        button_submit = soup.find('button', {'name': 'mark_as_read'})
        self.word_mark_as_read = button_submit['value']

    def mark_readed_report(self, id: int, toggle_state:int = 0):
        self.login.server_get('berichte.php', params={'id': id, 's': 0, 'toggleState': toggle_state})

    def delete_report(self, id: int):
        self.login.server_get('berichte.php', params={'n1': id, 'del': 1})

    def __get_reports_table(self, t: int=0, mode: str=None):
        params = {'t': t}
        if mode:
            params['opt'] = mode
        html = self.login.server_get('berichte.php', params=params)
        soup = bs4.BeautifulSoup(html, 'html5lib')
        li_reports = soup.find('li', {'class': 'reports'})
        div_content = li_reports.find('div', {'class': 'speechBubbleContent'})
        if div_content:
            report_number = int(div_content.text.strip('+'))
            print('new reports number:', report_number)
        form_reports = soup.find('form', {'id': 'reportsForm'})
        table_reports = form_reports.find('table', {'class': 'row_table_data'})
        return table_reports

    def clear(self):
        table_reports = self.__get_reports_table(0)
        table_body = table_reports.find('tbody')
        tr_reports = table_body.find_all('tr')
        if not tr_reports:
            return
        data = {
            'page': 1,
            'del': self.word_delete,
            's': '1'
        }
        for tr_report in tr_reports:
            if tr_report.find('td', {'class': 'noData'}):
                return
            td_sel = tr_report.find('td', {'class': 'sel'})
            input_check = td_sel.find('input', {'class': 'check'})
            report_name = input_check['name']
            report_id = int(input_check['value'])
            data[report_name] = report_id
        self.login.server_post('berichte.php', params={'t': 0}, data=data)
        self.clear()

    def mark_as_read_all(self):
        table_reports = self.__get_reports_table(0)
        table_body = table_reports.find('tbody')
        tr_reports = table_body.find_all('tr')
        if not tr_reports:
            return
        data = {
            'page': 1,
            'mark_as_read': self.word_mark_as_read,
            's': '1'
        }
        for tr_report in tr_reports:
            if tr_report.find('td', {'class': 'noData'}):
                return
            td_sel = tr_report.find('td', {'class': 'sel'})
            input_check = td_sel.find('input', {'class': 'check'})
            report_name = input_check['name']
            report_id = int(input_check['value'])
            data[report_name] = report_id
        self.login.server_post('berichte.php', params={'t': 0}, data=data)

    def get_reports(self):
        table_reports = self.__get_reports_table(0)
        table_head = table_reports.find('thead')
        table_body = table_reports.find('tbody')
        tr_reports = table_body.find_all('tr')
        print(len(tr_reports))

    def get_offensive_reports(self):
        reports = []
        table_reports = self.__get_reports_table(1, 'AAACAAMAAQA=')
        table_body = table_reports.find('tbody')
        tr_reports = table_body.find_all('tr')
        for tr_report in tr_reports:
            report = {}
            if tr_report.find('td', {'class': 'noData'}):
                return
            td_sel = tr_report.find('td', {'class': 'sel'})
            input_check = td_sel.find('input', {'class': 'check'})
            report_name = input_check['name']
            report['name'] = report_name
            report_id = int(input_check['value'])
            report['id'] = report_id
            l_find = lambda tag: tag.name == 'td' and tag.attrs and tag.attrs['class'][0] == 'sub'
            td_sub_newMessage = tr_report.find(l_find) # 'td', {'class': 'sub newMessage'})
            href_toggle_state = td_sub_newMessage.find('a')['href']
            report['href-toggle-state'] = href_toggle_state
            img_status = td_sub_newMessage.find('img', recursive=True)
            status_read = img_status['class'][1] == 'messageStatusRead'
            report['status-readed'] = status_read
            img_report = td_sub_newMessage.find('img', recursive=False)
            report_type = int(re.findall(r'(\d+)', img_report['class'][1])[0])
            report['report-type'] = report_type
            a_report_info = td_sub_newMessage.find('a', {'class': 'reportInfoIcon'})
            if a_report_info:
                img_info = a_report_info.find('img')
                action_type = img_info['class'][1]
                report['action type'] = action_type
            href_report = td_sub_newMessage.find('div', {'class': ''}).find('a')['href']
            report['href-report'] = href_report
            reports.append(report)
        return reports

    def get_defensive_reports(self):
        table_reports = self.__get_reports_table(2)

    def get_scouting_reports(self):
        table_reports = self.__get_reports_table(3)
        pass
