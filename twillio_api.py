from pprint import pprint
from twilio.rest import Client, TwilioClient
from twilio.twiml.voice_response import VoiceResponse, Say
import requests
import os
import json
import config
import time
# {"articles": [{"title": "description", "description": "dsvds", "body": "sdfbsfdvb", "author_id": 23}]}
# data = json.dumps({'articles': {"title": 'New state 2', "description": "About state 2",
#                                 "body": "Text state 2", "author_id": 2}})
# data = json.dumps('"articles":{"author_id": 534}')
#
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

# pprint(requests.post('https://803b-176-210-23-23.ngrok.io/', data=json.dumps({'name': 'dima', 'email': 'dima@mail.com'}),
#                      headers=headers).text)

# pprint(requests.get('https://803b-176-210-23-23.ngrok.io/').json())

# http://7539-176-210-23-23.ngrok.io

class Twilio:
    def __init__(self, account_sid, auth_token):
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.client = Client(self.account_sid, self.auth_token)

    def buy_number_phone(self):
        available_phone_numbers = self.client.available_phone_numbers('US').fetch().local.stream()
        for i in available_phone_numbers:
            number_sid = self.client.incoming_phone_numbers.create(phone_number=i.phone_number)

    def update_number(self, url):
        for number in self.client.incoming_phone_numbers.stream():
            self.client.incoming_phone_numbers(number.sid).update(voice_url=url)

    def create_sip_domain(self):
        sid_credential_lists = self.client.sip.credential_lists.create(friendly_name='sergeyi').sid
        self.client.sip.credential_lists(sid_credential_lists).credentials.create(username='sergeyi', password='vovavovavovaA1')
        domain = self.client.sip.domains.create(domain_name='sergeyi7.sip.ashburn.twilio.com',
                                                friendly_name='sergeyi', sip_registration=True)
        self.client.sip.domains(domain.sid).auth.registrations.credential_list_mappings.create(sid_credential_lists)
        self.client.sip.domains(domain.sid).auth.calls.credential_list_mappings.create(sid_credential_lists)

    def get_credentialList(self):
        list_credentialList = []
        for i in self.client.sip.domains.stream():
            for k in i.credential_list_mappings.stream():
                list_credentialList.append('friendly name -> ' + k.friendly_name)
        return list_credentialList

    def get_friendly_name(self):
        for i in self.client.sip.ip_access_control_lists.stream():
            return i.friendly_name

    def all_delete(self):
        for i in self.client.sip.domains.stream():
            i.delete()
        for i in self.client.sip.credential_lists.stream():
            i.delete()

    def call(self, url, from_, to):
        response = VoiceResponse()
        response.say('Привет, это бот говорит. Скоро мы вас захватим!!! ХАХАХАХАХАХ', language='ru-RU')

        call = self.client.calls.create(twiml=response.to_xml(),
                                        # method='GET',
                                        # send_digits='14154834991',
                                        status_callback=url,
                                        status_callback_event=['completed'],
                                        status_callback_method='POST',
                                        to=to,
                                        from_=from_)
                                        # to='sip:sergeyi@sergeyi7.sip.twilio.com',
                                        # from_='+12542795665')

        return call

    def call2(self, url, from_, to):
        response = VoiceResponse()
        response.dial('+14154834991')
        return self.client.calls.create(twiml=response.to_xml(xml_declaration=False),
                                        url=url,
                                        to=to,
                                        from_=from_).status

    def call3(self):
        response = VoiceResponse()
        response.say('Привет, это бот говорит. Скоро мы вас захватим!!! ХАХАХАХАХАХ', language='ru-RU')
        # response.dial('+14154834991')
        #'sip:sergeyi@sergeyi7.sip.twilio.com'
        # response.dial('+12542795665')
        return self.client.calls.create(twiml=response.to_xml(),
                                        from_='sip:@sergeyi7.sip.ashburn.twilio.com',
                                        to='+12542795665',
                                        sip_auth_username='sergeyi',
                                        sip_auth_password='vovavovavovaA1').status

    def call4(self):
        self.my_number()
        for i in self.client.calls(self.number_sid).events.stream():
            print(i.request)

    def get_sip_domain_name(self):
        for i in self.client.sip.domains.stream():
            return i.domain_name

    def my_number(self):
        for i in self.client.incoming_phone_numbers.local.stream():
            self.number_sid = i.sid
            return i.phone_number



#vovavovavovaA1
# twil = Twilio(config.twilio_account_sid, config.twilio_auth_token)
# twil.call3()

# twil.create_sip_domain()
# twil.all_delete()
# twil.buy_number_phone()
# print(twil.my_number())
# twil.get_friendly_name()
# print(twil.get_credentialList())
# print(twil.registration_probe_credential_list_mappings())

# twil.call()

# twil.call2(url='https://48d8-8-21-110-27.ngrok.io/probe/', to='sip:sergeyi@sergeyi7.sip.twilio.com',
#            from_='+12542795665')

# print(requests.get('https://48d8-8-21-110-27.ngrok.io/probe/').text)

# twil.get_sip_domain_name()

