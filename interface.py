import requests
import amo_api
import twillio_api
import config
from pprint import pprint

#################TODO 1 Задание##################################
# names = ['Дима', 'Вова', 'Маша', 'Андрей', 'Лена', 'Алёна', 'Сергей', 'Алексей', 'Женя', 'Боб']
# code = 'def502007c65059fb35c34a13a1b7fa3a683295a7f6edb0965396703016eaa8edfcce767add8efa295123bcdbc6c8e879f1ccc0d06f39ceb1792ad44978c1ccd6b5d3c2a61846f48688d2b9e2036bb73e054d0d68ae466736b8517da4392a7d3131bc9bc33070f6ba1defcb8f61234c77b58ede0607554164657cbbd5258b2ffd3222ba63ef95e6bbbfd58b44190bb31b06062a4e1ad82b37f1f25949ccf0979e6fba72919f1f313736690fde53d963da694521132159f15606870f683b0faebcd5cc2c2f1d48ef147290041e4f158fc99acfe52028ee003d9495f8189016b74491bb0cf810818391fa4f61be7a5fb680af3d0eae9fc97028ab2644eaaeb8b8ec8ebc848b4860959c66fecfc29733f96f93cc56425c000f623ac2e9cb2d8473ab090c6d22ab5e871cc64fd9cbcc3806a8468314ce31653dc2fb051307e5101cded0128e0c7b2e83f75ebf8b121e7488533df610b397eaec229b9e23ce15947ec1e3f6bf96aafcd31094df2cb85a9b0a462e26ab477236013471001fc4397d21b7c4514cda0927c8dafb3e3dcca0155e5d34fb730d906dcbfa2f9bcc495b31fd8d8c6460291c290cd2328e7eacd14105a72d9edc92dc7eaf06f339a414a6db1c53846aa1b8dad5f64'
# amo = amo_api.Amo(config.amo_secret_key, config.amo_integration_key, config.amo_redirect_url,
#                   config.amo_my_url, config.amo_subdomain)
# amo.set_refresh_token(code)
# amo.conn()
# amo.ten_contacts_leads(names, 'poleshhuk97@gmail.com', '+12542795471', 'Moscow, Pushkina, 1')
# pprint(amo.get_all_contacts_leads())
# amo.session_lead(mail=config.amo_mail, password=config.amo_password)
###################################################################

#################TODO 2 Задание##################################
# tw = twillio_api.Twilio(config.twilio_account_sid, config.twilio_auth_token)
# tw.update_voice_urls('https://48d8-8-21-110-27.ngrok.io/answer/')
# tw.buy_number_phone()
# tw.all_delete()
# tw.create_sip_domain()
# tw.call(url='https://48d8-8-21-110-27.ngrok.io/probe', from_='+12542795665', to='sip:sergeyi@sergeyi7.sip.twilio.com')
# tw.call2(url='https://48d8-8-21-110-27.ngrok.io/probe', from_='+12542795665', to='sip:sergeyi@sergeyi7.sip.twilio.com')
###################################################################


# #################TODO 3 Задание##################################
#
# class Caller:
#     def __init__(self):
#         self.amo = amo_api.Amo(config.amo_secret_key, config.amo_integration_key, config.amo_redirect_url,
#                                config.amo_my_url, config.amo_subdomain)
#         code = 'def50200b1f12f006610c442ac477aae1a336cf41e7aa02a97df8685c1d24b78b48576aa3a741dd9b69a071e74d08d1235e291ede0666531cf18721a9506f44f2da51f575a6f71c2f324f6fef60d70c18c7dd08619ad07456410c347fbb39bd1d153229e0f76b3783c8878e696d3f5edd8960770905efcaa161ee062849217189fe0d183800f088751bdf6949e415d726e4ee531fb5cd0e237e3a779dd5548f2e05608423816d3d94192a83f5f6745fd78b89565d192a89d3630b0724b42f15ffc0cad4f2a305e650cb5c52dc27b97d4dbc2553b09b719aa9f52af403cdfd4782e9decde45dffb425379696aa3fe6b9ada386fc957916dc3c036ae210bd004298d703fd9bb75401c8abe0ce5935d39a946c769e5e0285008b8d371ae2067123ad55de0b206117416b573b8895225f616989c9700485fbb3bfe78c565eb9cd67c8aee372ee79737069dcef09ef113506e6debfb48f77292f953e6c8cf38692fd039b719aa73326a25e4ad9c0ceb42745700b991b262be2d6ff4d9c6726d79ad9bda3d22f9a3cc69ba7c146d8132e7f103cee3d9038844373628afecc0f3ac67dc8023e60559f93c01d7d8e318a9f746e84ab39e4b2080913ab793f4563d00fc41a8f63f170be29d6b'
#         # self.amo.set_refresh_token(code)
#         self.amo.conn()
#         self.tw = twillio_api.Twilio(config.twilio_account_sid, config.twilio_auth_token)
#
#     def incoming(self, public_url, to_name):
#         while True:
#             s = requests.Session()
#             s_get = s.get(f'{public_url}/answer/').text
#             if s_get.replace('\n', '') == 'true':
#                 self.amo.add_notes(to_name, type_call='in')
#                 print('Звонок завершён!')
#                 break
#         requests.patch(f'{public_url}/answer/1', json={'status': False})
#
#     def outgoing(self, public_url, to_name):
#         self.tw.call(f'{public_url}/probe/', from_='+12542795665', to='sip:sergeyi@sergeyi7.sip.twilio.com')
#         while True:
#             s = requests.Session()
#             s_get = s.get(f'{public_url}/probe/').text
#             if s_get.replace('\n', '') == 'true':
#                 self.amo.add_notes(to_name, type_call='out')
#                 print('Звонок завершён!')
#                 break
#         requests.patch(f'{public_url}/probe/1', json={'status': False})
#
#
# call = Caller()
# # call.outgoing('https://48d8-8-21-110-27.ngrok.io', 'Андрей')
# call.incoming('https://48d8-8-21-110-27.ngrok.io', 'Андрей')

