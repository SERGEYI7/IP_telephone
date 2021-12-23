from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Say
import os
import config

response = VoiceResponse()
response.dial('+12542795665')
response.say('Hello world')
print(response)


class Twilio:
    def __init__(self, account_sid, auth_token):
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.client = Client(self.account_sid, self.auth_token)

    def buy_number_phone(self):
        available_phone_numbers = self.client.available_phone_numbers('US').fetch().local.stream()
        for i in available_phone_numbers:
            self.client.incoming_phone_numbers.create(phone_number=i.phone_number)

    def create_sip_domain(self):
        sid_credential_lists = self.client.sip.credential_lists.create(friendly_name='sergeyi').sid
        self.client.sip.credential_lists(sid_credential_lists).credentials.create(username='sergeyi', password='vovavovavovaA1')
        # self.client.sip.credential_lists.
        sid_domain = self.client.sip.domains.create(domain_name='sergeyi7.sip.ashburn.twilio.com',
                                                    friendly_name='sergeyi', sip_registration=True).sid
        self.client.sip.domains(sid_domain).auth.registrations.credential_list_mappings.create(sid_credential_lists)
        self.client.sip.domains(sid_domain).auth.calls.credential_list_mappings.create(sid_credential_lists)
        # sid_mapping_credential_lists = self.client.sip.domains(sid_domain).credential_list_mappings(sid_credential_lists)
        # self.client.sip.domains(sid_domain).auth.registrations.credential_list_mappings(sid_mapping_credential_lists)

        # self.client.sip.domains(sid_domain).credential_list_mappings.create(sid_credential_lists)
        # self.client.sip.domains(sid_domain).auth.registrations.credential_list_mappings(sid_credential_lists)

    # def create_credentialList(self):
    #     for i in self.client.sip.domains.stream():
    #         print(i.sid)
    #         new_sid = self.client.sip.credential_lists.create(friendly_name='ser').sid
    #         self.client.sip.domains(i.sid).credential_list_mappings.create(new_sid)
    #     print(i.friendly_name)
    #     self.client.sip.credential_lists.create(friendly_name='sergeyi')

    def get_credentialList(self):
        list_credentialList = []
        for i in self.client.sip.domains.stream():
            for k in i.credential_list_mappings.stream():
                list_credentialList.append('friendly name -> ' + k.friendly_name)
        return list_credentialList

    def get_friendly_name(self):
        for i in self.client.sip.ip_access_control_lists.stream():
            return i.friendly_name

    # def registration_sip_domain(self):
    #     for i in self.client.sip.domains.stream():
    #         print(i.sip_registration)

    # def registration_probe_credential_list_mappings(self):
    #     for i in self.client.sip.domains.stream():
    #         for j in i.credential_list_mappings.stream():
    #             rgs = self.client.sip.domains(i) \
    #                 .auth \
    #                 .registrations \
    #                 .credential_list_mappings(j)
    #             return rgs.fetch()

    def all_delete(self):
        for i in self.client.sip.domains.stream():
            i.delete()
        for i in self.client.sip.credential_lists.stream():
            i.delete()

    def call(self):
        self.client.calls.create(url='https://demo.twilio.com/welcome/voice/',
                                 to='sip:sergeyi@sergeyi7.sip.twilio.com',
                                 from_='sergeyi',
                                 sip_auth_username='sergeyi',
                                 sip_auth_password='vovavovavovaA1')


    def get_sip_domain_name(self):
        for i in self.client.sip.domains.stream():
            return i.domain_name

    def my_number(self):
        for i in self.client.incoming_phone_numbers.local.stream():
            return i.phone_number

    # def sms(self):
    #     self.client.messages.create(to='+79618848116', from_='+12542795665', body='Привет мляха муха')


#vovavovavovaA1
twil = Twilio(config.twilio_account_sid, config.twilio_auth_token)
# twil.create_sip_domain()
# twil.all_delete()
# twil.buy_number_phone()
# print(twil.my_number())
# twil.get_friendly_name()
# twil.create_sip_domain()
# twil.create_credentialList()
# print(twil.get_credentialList())
# print(twil.registration_probe_credential_list_mappings())
twil.call()

# print(twil.call3())
# twil.registration_sip_domain()
# twil.get_sip_domain_name()
# twil.sms()

