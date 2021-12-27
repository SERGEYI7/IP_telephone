import smtplib
from time import sleep
import re
import datetime
import requests
import json
import config


class Amo:

    def __init__(self, secret_key, integration_key, redirect_url, my_url, subdomain):
        self.secret_key = secret_key
        self.integration_key = integration_key
        self.redirect_url = redirect_url
        self.my_url = my_url
        self.subdomain = subdomain
        self.headers = ''
        self.names_ids = {}
        self.data_get_refresh_token =\
            {"client_id": integration_key,
             "client_secret": secret_key,
             "grant_type": "authorization_code",
             "code": '',
             "redirect_uri": redirect_url}
        self.data_get_access_token = \
            {"client_id": integration_key,
             "client_secret": secret_key,
             "grant_type": "refresh_token",
             "refresh_token": '{refresh_token}',
             "redirect_uri": redirect_url}

    def conn(self):
        self.data_get_access_token.update({"refresh_token": self._get_refresh_with_json_()})
        response = requests.post(f'https://{self.subdomain}.amocrm.com/oauth2/access_token', self.data_get_access_token)
        access_token = response.json()['access_token']
        self.headers = {'Authorization': 'Bearer '+access_token}
        response = requests.get(f'https://{self.subdomain}.amocrm.com/api/v2/account',  headers=self.headers).json()
        return response

    def add_contact(self, name, mail, phone, position):
        data = json.dumps({'add': [{'name': name, 'custom_fields': [{'id': 237023, 'values': [{'value': position}, ]},
                                                                    {'id': 237027, 'values': [{'value': mail,
                                                                                               'enum': 166959}]},
                                                                    {'id': 237025, 'values': [{'value': phone,
                                                                                               'enum': 166947}]}]}]})
        response = requests.post(f'https://{self.subdomain}.amocrm.com/api/v2/contacts', data=data, headers=self.headers).json()
        return response

    def add_lead(self, name, ids):
        data = json.dumps({'name': name,
                           'add': [{'contacts_id': [ids]}]
                           })
        response = requests.post(f'https://{self.subdomain}.amocrm.com/api/v2/leads', data=data,
                                 headers=self.headers).json()
        return response['_embedded']['items'][0]['id']

    def get_contact_by_id(self, ids):
        response = requests.get(f'https://{self.subdomain}.amocrm.com/api/v2/contacts', params={'id': ids},
                                headers=self.headers).json()
        return response

    def ten_contacts_leads(self, names: list, mail, phone, position):
        for name in names:
            ids_contact = self.add_contact(name, mail, phone, position)['_embedded']['items'][0]['id']
            ids_lead = self.add_lead(name, ids_contact)
            status_id = requests.get(f'https://{self.subdomain}.amocrm.com/api/v2/leads/?id={ids_lead}',
                                     headers=self.headers).json()['_embedded']['items'][0]['status_id']
        #     self.names_ids[name] = {'id_contact': ids_contact, 'id_lead': ids_lead, 'status_id': status_id}
        # return self.names_ids

    def set_refresh_token(self, code):
        with open('access_refresh.json', 'w', encoding='utf8') as f_amo:
            self.data_get_refresh_token.update({'code': code})
            response = requests.post(f'https://{self.subdomain}.amocrm.com/oauth2/access_token',
                                     self.data_get_refresh_token)
            refresh_token = response.json()['refresh_token']
            json.dump({'refresh_token': refresh_token}, f_amo)

    def session_lead(self, mail, password):
        names_ids = self.get_all_contacts_leads()
        s = requests.Session()
        smtp_re = re.findall(r'.*?@(.*?)$', mail)[0]
        smtp_obj = smtplib.SMTP(f'smtp.{smtp_re}', 587)
        smtp_obj.starttls()
        smtp_obj.login(mail, password)
        while True:
            sleep(0.1)
            for i in names_ids.items():
                name = i[0]
                id_contact = i[1]['id_contact']
                id_lead = i[1]['id_lead']
                status_id_old = i[1]['status_id']
                status_id_new = s.get(f'https://{self.subdomain}.amocrm.com/api/v2/leads/?id={id_lead}',
                                      headers=self.headers).json()['_embedded']['items'][0]['status_id']
                if status_id_new != status_id_old:
                    names_ids[name]['status_id'] = status_id_new
                    date_for_tasks = datetime.datetime.now() + datetime.timedelta(hours=23)
                    data = json.dumps({'add': [{'element_id': id_contact,
                                                'element_type': 1,
                                                'task_type': 3,
                                                'text': f'Name contact - {name}',
                                                'complete_till_at': date_for_tasks.timestamp()}]})
                    post_tasks = s.post(f'https://{self.subdomain}.amocrm.com/api/v2/tasks', data=data,
                                        headers=self.headers).json()
                    data = json.dumps({'add': [{'element_id': id_contact,
                                                'element_type': 1,
                                                'text': 'change status lead',
                                                'note_type': 4}]})
                    post_notes = s.post(f'https://{self.subdomain}.amocrm.com/api/v2/notes', headers=self.headers,
                                        data=data)
                    smtp_obj.sendmail(msg=f'Date - {date_for_tasks.date()}\n'
                                          f'Time - {date_for_tasks.time().hour}:{date_for_tasks.time().minute}:00\n'
                                          f'Duration - {30} minutes\n'
                                          f'Addres - Moscow, Pushkina, 3'.encode(), from_addr=mail,
                                          to_addrs=names_ids[name]['mail_contact'])

    def add_notes(self, name: str, type_call: str):
        if type_call == 'in':
            num_type = 10
        elif type_call == 'out':
            num_type = 11
        else:
            raise Exception('Введит входящий (in) или исходящий (out) тип звонка')
        names_ids = self.get_all_contacts_leads()
        id_contact = names_ids[name]['id_contact']
        data = json.dumps({'add': [{'element_id': id_contact,
                                    'element_type': 1,
                                    'text': 'Phone call ended.',
                                    'note_type': num_type}]})
        requests.post(f'https://{self.subdomain}.amocrm.com/api/v2/notes', headers=self.headers,
                      data=data)

    def _get_code_with_json_(self):
        with open('access_refresh.json', 'r', encoding='utf8') as f_amo:
            access_token = json.load(f_amo)['access_token']
        return access_token

    def _get_refresh_with_json_(self):
        with open('access_refresh.json', 'r', encoding='utf8') as f_amo:
            refresh_token = json.load(f_amo)['refresh_token']
        return refresh_token

    def get_all_contacts_leads(self):
        names_ids = {}
        s = requests.Session()
        response_leads = s.get(f'https://{self.subdomain}.amocrm.com/api/v2/leads', params={'limit_rows': 100},
                               headers=self.headers).json()
        for lead in response_leads['_embedded']['items']:
            id_contact = lead['contacts']['id'][0]
            response_contact = s.get(f'https://{self.subdomain}.amocrm.com/api/v2/contacts', params={'id': id_contact},
                                 headers=self.headers).json()
            name_contact = response_contact['_embedded']['items'][0]['name']
            mail_contact = response_contact['_embedded']['items'][0]['custom_fields'][1]['values'][0]['value']
            phone_contact = response_contact['_embedded']['items'][0]['custom_fields'][2]['values'][0]['value']
            names_ids[name_contact] = {'id_contact': id_contact, 'id_lead': lead['id'],
                                       'status_id': lead['status_id'], 'mail_contact': mail_contact,
                                       'phone_contact': phone_contact}
        return names_ids

# am = Amo(secret_key=secret_key, integration_key=integration_key, redirect_url=redirect_url, my_url=my_url)
# # am.set_refresh_token(code)
# am.conn()
# # am.ten_contacts_leads(names, 'poleshhuk97@gmail.com', '112233444555', 'Moscow, Pushkina, 1')
# # am.add_contact('6 Иван Дмитрий')
# # pprint(am.get_contact_by_id(752367))
# am.session_lead(mail=config.amo_mail, password=config.amo_password)
