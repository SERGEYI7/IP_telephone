import smtplib
from time import sleep
import re
import datetime
import requests
import json
import config


class Amo:

    def __init__(self, secret_key, integration_key, redirect_url, my_url):
        self.secret_key = secret_key
        self.integration_key = integration_key
        self.redirect_url = redirect_url
        self.my_url = my_url
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
        response = requests.post('https://poleshhuk97mailru.amocrm.com/oauth2/access_token', self.data_get_access_token)
        access_token = response.json()['access_token']
        self.headers = {'Authorization': 'Bearer '+access_token}
        response = requests.get('https://poleshhuk97mailru.amocrm.com/api/v4/account',  headers=self.headers).json()
        return response

    def add_contact(self, name, mail, phone, position):
        data = json.dumps({'add': [{'name': name, 'custom_fields': [{'id': 237023, 'values': [{'value': position}, ]},
                                                                    {'id': 237027, 'values': [{'value': mail,
                                                                                               'enum': 166959}]},
                                                                    {'id': 237025, 'values': [{'value': phone,
                                                                                               'enum': 166947}]}]}]})
        response = requests.post('https://poleshhuk97mailru.amocrm.com/api/v2/contacts', data=data, headers=self.headers).json()
        return response

    def add_lead(self, name, ids):
        data = json.dumps({'name': name,
                           'add': [{'contacts_id': [ids]}]
                           })
        response = requests.post('https://poleshhuk97mailru.amocrm.com/api/v2/leads', data=data,
                                 headers=self.headers).json()
        return response['_embedded']['items'][0]['id']

    def get_contact_by_id(self, ids):
        response = requests.get(f'https://poleshhuk97mailru.amocrm.com/api/v2/contacts', params={'id': ids},
                                headers=self.headers).json()
        return response

    def ten_contacts_leads(self, names: list, mail, phone, position):
        for i in names:
            ids_contact = self.add_contact(i, mail, phone, position)['_embedded']['items'][0]['id']
            ids_lead = self.add_lead(i, ids_contact)
            status_id = requests.get(f'https://poleshhuk97mailru.amocrm.com/api/v2/leads/?id={ids_lead}',
                                     headers=self.headers).json()['_embedded']['items'][0]['status_id']
            self.names_ids[i] = {'id_contact': ids_contact, 'id_lead': ids_lead, 'status_id': status_id}
        return self.names_ids

    def set_refresh_token(self, code):
        with open('access_refresh.json', 'w', encoding='utf8') as f_amo:
            self.data_get_refresh_token.update({'code': code})
            response = requests.post('https://poleshhuk97mailru.amocrm.com/oauth2/access_token',
                                     self.data_get_refresh_token)
            refresh_token = response.json()['refresh_token']
            json.dump({'refresh_token': refresh_token}, f_amo)

    def session_lead(self, mail, password):
        self.get_all_contacts_leads()
        s = requests.Session()
        smtp_re = re.findall(r'.*?@(.*?)$', mail)[0]
        smtp_obj = smtplib.SMTP(f'smtp.{smtp_re}', 587)
        smtp_obj.starttls()
        smtp_obj.login(mail, password)
        while True:
            sleep(0.1)
            for i in self.names_ids.items():
                name = i[0]
                id_contact = i[1]['id_contact']
                id_lead = i[1]['id_lead']
                status_id_old = i[1]['status_id']
                status_id_new = s.get(f'https://poleshhuk97mailru.amocrm.com/api/v2/leads/?id={id_lead}',
                                      headers=self.headers).json()['_embedded']['items'][0]['status_id']
                if status_id_new != status_id_old:
                    self.names_ids[name]['status_id'] = status_id_new
                    date_for_tasks = datetime.datetime.now() + datetime.timedelta(hours=23)
                    data = json.dumps({'add': [{'element_id': id_contact,
                                                'element_type': 1,
                                                'task_type': 3,
                                                'text': f'Name contact - {name}',
                                                'complete_till_at': date_for_tasks.timestamp()}]})
                    post_tasks = s.post(f'https://poleshhuk97mailru.amocrm.com/api/v2/tasks', data=data,
                                        headers=self.headers).json()
                    data = json.dumps({'add': [{'element_id': id_contact,
                                                'element_type': 1,
                                                'text': 'change status lead',
                                                'note_type': 4}]})
                    post_notes = s.post('https://poleshhuk97mailru.amocrm.com/api/v2/notes', headers=self.headers,
                                        data=data)
                    smtp_obj.sendmail(msg=f'Date - {date_for_tasks.date()}\n'
                                          f'Time - {date_for_tasks.time().hour}:{date_for_tasks.time().minute}:00\n'
                                          f'Duration - {30} minutes\n'
                                          f'Addres - Moscow, Pushkina, 3'.encode(), from_addr=mail,
                                          to_addrs=self.names_ids[name]['mail_contact'])

    def _get_code_with_json_(self):
        with open('access_refresh.json', 'r', encoding='utf8') as f_amo:
            access_token = json.load(f_amo)['access_token']
        return access_token

    def _get_refresh_with_json_(self):
        with open('access_refresh.json', 'r', encoding='utf8') as f_amo:
            refresh_token = json.load(f_amo)['refresh_token']
        return refresh_token

    def get_all_contacts_leads(self):
        s = requests.Session()
        response_leads = s.get(f'https://poleshhuk97mailru.amocrm.com/api/v2/leads', params={'limit_rows': 100},
                               headers=self.headers).json()
        for lead in response_leads['_embedded']['items']:
            id_contact = lead['contacts']['id'][0]
            response_contact = s.get(f'https://poleshhuk97mailru.amocrm.com/api/v2/contacts', params={'id': id_contact},
                                 headers=self.headers).json()
            name_contact = response_contact['_embedded']['items'][0]['name']
            mail_contact = response_contact['_embedded']['items'][0]['custom_fields'][1]['values'][0]['value']
            self.names_ids[name_contact] = {'id_contact': id_contact, 'id_lead': lead['id'],
                                            'status_id': lead['status_id'], 'mail_contact': mail_contact}
        return self.names_ids


secret_key = 'iDC5QRNb9XKHjbBzwcZPEL4R0ZxGoJ8MuOtAEzbkJ7RiuV7XJPPV02LbVq2OQqQJ'
integration_key = '7b74a8fe-da38-4592-ba6c-9547a4cbeca3'
redirect_url = 'https://poleshhuk97.amocrm.com'
code = 'def50200dd6ca018a3cd06b4899952533d351874c3c0abb1d1a967f46a2fb04232b748904805c3c86400fc896c4849f1e58213e22c89e1faa0de447f062422efaaca2aeccf2eb82aaf3fc6f14f6f0e28482af10c9cef0b5b52ef1b781212a388b3d9877db8c1b2c51f3fed4a3574aabbb5ad8290447efebe0396f1a63f645acf28334d368db4f7d90092502f2f6140c264d6d15162e2810caa2f90d7d35b686a257e5fa3bce3b4e81c50e3a1354619b394eb6d2ed6f2709bf8c1894a069be68959137a43cb6dee63f02f13f9a6af06cf47756388f1826391e870e056dc7286a39f701cb57c901905b4c8c3e36f0771365b1b4f0a10494155e31f35734bcc951af7282ce325bba2b76dbcec16d83e44477a61cfba688e4b8619c6e1103905a802874fd70985939c1cd571758e99520a12edfef8c551b24380fc89b1ff393c0e8c266feaddda27fc242cc9feb7ed087c4c85e0b5a779e7f85889590545c72ab29181fc5dc968e4d3701eafbabb223c99fa40cd22d72b8dc5515da6744c8bce0e75c9cbf87419323f0fb4880b8371d61c7247846202cd4cc003858dba676b5ebbe387228569213c7912163eaf93e3929d51cbada023334a4533967dd3a7802b9c8b0aebad2ba396513f'
my_url = 'https://poleshhuk97mailru.amocrm.com/api/v2/account/'
names = ['Дима', 'Вова', 'Маша', 'Андрей', 'Лена', 'Алёна', 'Сергей', 'Алексей', 'Женя', 'Боб']
am = Amo(secret_key=secret_key, integration_key=integration_key, redirect_url=redirect_url, my_url=my_url)
# am.set_refresh_token(code)
am.conn()
# am.ten_contacts_leads(names, 'poleshhuk97@gmail.com', '112233444555', 'Moscow, Pushkina, 1')
# am.add_contact('6 Иван Дмитрий')
# pprint(am.get_contact_by_id(752367))
am.session_lead(mail=config.mail, password=config.password)
