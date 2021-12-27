import json
from pprint import pprint

import requests

import amo_api
import twillio_api
import flask_app
import config

#################TODO 1 Задание##################################
# names = ['Дима', 'Вова', 'Маша', 'Андрей', 'Лена', 'Алёна', 'Сергей', 'Алексей', 'Женя', 'Боб']
# code = 'def50200b246b20d6fd2732c3eaa2a094cd3959acf1c479a07ffca60259a07153d6551e4c14e7aada517c86e1e20cc461d5e7f2f3196bca3b82878607add92dd78adf38e37dfba49f0ed3066841d5f3392e740440b0ca32e373f196f18028895b7e80a17d5caf960269e4bdb868ad14c0f1c7d838a3e76d6dea42b79064fe3b114b264929be45ffb38af82a445447fe4dc171602961420cbb2a0a6876667f511dbe91f70dc536572caf1c477cfb756cc20162ab25773f01116915c70d5cfe3799fa62c4ceddf1b446c7cb75eb6b68b3c059da70e53f8f66034bae08a9505846c243b122cf9910b59e6169fb10c0f949bbb80fe2e52c50e025310a455ebce6e8f5cbc152fc858b02d4ffab301f89467a9cd41fbe1bbab3e934ca1ed5ed73f90c5bb1da868ebb0abe2191be17c563015492937b277892ac1ed13d687ab6aade330bdb35ddb62be893dd4393d9bd99b55e52a9d48ec374c26f53c58950aac4a2fcc2efeb881978d283951e77895921daedc03b682862e501bd40ba87975e5ed48f60c53d24d05c2972fc1ad51297cf4a815809fe4abcf6fe11ec78b070962da695b3221dd6a645ee715d3f2a1881f7e5397023cf19e4c95d18e03f2a6b4931d0a4c92ffdfd8705ddba2'
# amo = amo_api.Amo(config.amo_secret_key, config.amo_integration_key, config.amo_redirect_url,
#                   config.amo_my_url, config.amo_subdomain)
# # amo.set_refresh_token(code)
# amo.conn()
# amo.ten_contacts_leads(names, 'poleshhuk97@gmail.com', '+12542795471', 'Moscow, Pushkina, 1')
# pprint(amo.get_all_contacts_leads())
###################################################################

#################TODO 2 Задание##################################
# tw = twillio_api.Twilio(config.twilio_account_sid, config.twilio_auth_token)
# tw.update_number('https://48d8-8-21-110-27.ngrok.io/answer/')
# tw.buy_number_phone()
# tw.all_delete()
# tw.create_sip_domain()
# tw.call2()
###################################################################


#################TODO 3 Задание##################################

# class Caller:
#     def __init__(self):
#         self.amo = amo_api.Amo(config.amo_secret_key, config.amo_integration_key, config.amo_redirect_url,
#                                config.amo_my_url, config.amo_subdomain)
#         code = 'def50200e30f80733cb5dd398548bb40cc6bfe6fa169436d16d6304feb349b52c6dfe01948f918e5caf9017b5e6046bde1b40afe44b6eacc744c9d6d22a8fe89df6fcf1abe42e51b47b4e091a5aee477c3d08f841c97d73fcd1a3a15ba396d2423463d7c52995804a6d1e06926b970839bda4356f7deba7eb02e49f6b9789ec2d0af2ddee481b6aa6d325ecf7a6efc96737ce9e12e2146a425375fce2a2120c7061cbdd27cb39c4eeefed1667391906a0b5c39881744f14a1328dfb5aab07184f3f98e05ba1cf88192880171b4831fdb1785d869c50f5216255e723add16f96239d6543f8aebdb750dd3103330beb161e27f9f9f3c6d5ff6c464b23d135da16da6bbce63720d41b9b090ff96d7c183fb327ffd4f64f66129dd06135d5d56026c4d95898527edeb3c0df63167bc71f4bdb59156f1613147af17bdc5db7f8c7f3b85658486f3f67ab0f02f136db0e16e278d209835ab264d64121c7ac88a43b5bcf1434ff0fdacf34e3d4267aeb75c77e8daa56089e3f0c3da31c12bc266b14edb9faee6b5183d4115034e05301b0399959866de7e94766b200ee5f20ccd2e2b0a4262ce08ce7d7b67cdca530113b2c8a1f41e98f3be3f997614c8c0d993d61ec7b0155842e34519bf'
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
# # call.outgoing('https://48d8-8-21-110-27.ngrok.io', 'Женя')
# call.incoming('https://48d8-8-21-110-27.ngrok.io', 'Женя')

