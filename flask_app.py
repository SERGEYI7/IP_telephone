from flask import Flask
from flask import request, abort, jsonify
from twilio.twiml.voice_response import VoiceResponse
import json

app = Flask(__name__)

probe = {'id': 1, 'status': False}


@app.route('/probe/<id>', methods=['PATCH'],)
def patch_probe(id):
    req = request.get_json()
    for i in req:
        print(i)
    global probe
    probe = req
    return jsonify({'status': 'Молодец'}, probe)


@app.route('/probe/', methods=['POST', 'GET'])
def create_probe():
    if request.method == 'POST':
        if not request.json:
            # print(request.content_encoding)
            probe['status'] = True
            respp = {'status': probe['status']}
            print(respp)
        print('Тут что то есть?')
        return jsonify(respp, 201)
    elif request.method == 'GET':
        return jsonify(probe['status'])


answer = {'id': 1, 'status': False}
@app.route('/answer/', methods=['GET', 'POST', 'PATCH'])
def answer_call():
    if request.method == 'POST':
        resp = VoiceResponse()
        resp.say('Узбекистан, шымкент, Боровое', voice='alice', language='ru-RU')
        answer['status'] = True
        print('Есть что?')
        return str(resp)
    elif request.method == 'PATCH':
        answer['status'] = False
    elif request.method == 'GET':
        return jsonify(answer['status'])

@app.route('/answer<id>', methods=['PATCH'])
def answer_patch(id):
    req = request.get_json()
    for i in req:
        print(i)
    global answer
    answer = req
    return jsonify({'status': 'Молодец'}, answer)

if __name__ == "__main__":
    app.run(port=8000)
