from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Say
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}


class Twilio:
    def __init__(self, account_sid, auth_token):
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.client = Client(self.account_sid, self.auth_token)

    def buy_number_phone(self):
        available_phone_numbers = self.client.available_phone_numbers('US').fetch().local.stream()
        for i in available_phone_numbers:
            number_sid = self.client.incoming_phone_numbers.create(phone_number=i.phone_number)
            return

    def update_voice_urls(self, url):
        for number in self.client.incoming_phone_numbers.stream():
            for domain in self.client.sip.domains.stream():
                self.client.incoming_phone_numbers(number.sid).update(voice_url=url)
                self.client.sip.domains(domain.sid).update(voice_url=url)

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
                                        to=to,
                                        from_=from_)

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

