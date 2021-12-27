from flask import Flask
from flask import request, abort, jsonify
from twilio.twiml.voice_response import VoiceResponse

app = Flask(__name__)

tasks = [
    {"id": 1,
     "name": "vova",
     "email": "vova@mail.ru"}
]

probe = {'id': 1, 'status': False}


@app.route("/voice", methods=['GET', 'POST'])
def voice():
    if not request.json or not 'title' in request.json:
        abort(400)

    """Respond to incoming phone calls with a 'Hello world' message"""
    # Start our TwiML response
    resp = VoiceResponse()

    # Read a message aloud to the caller
    resp.say("hello world!", voice='alice')

    return str(resp)


# @app.route('/', methods=['GET'])
# def get_tasks():
#     return jsonify(tasks, probe_post)


# @app.route('/', methods=['POST'])
# def create_task():
#     if not request.json or not 'name' in request.json:
#         abort(400)
#     task = {'id': tasks[-1]['id'] + 1,
#             'name': request.json['name'],
#             'email': request.json['email']}
#     tasks.append(task)
#     return jsonify({'task': task}), 201


@app.route('/probe/<id>', methods=['PATCH'],)
def patch_probe(id):
    req = request.get_json()
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
        return jsonify(respp, 201)
    elif request.method == 'GET':
        return jsonify(probe['status'])


answer = {'id': 1, 'status': False}
@app.route('/answer/', methods=['GET', 'POST'])
def answer_call():
    if request.method == 'POST':
        resp = VoiceResponse()
        resp.say('Узбекистан, шымкент, Боровое', voice='alice', language='ru-RU')
        answer['status'] = True
        return str(resp)
    elif request.method == 'GET':
        return jsonify(answer['status'])

@app.route('/answer<id>', methods=['PATCH'])
def answer_patch(id):
    req = request.get_json()
    global answer
    answer = req
    return jsonify({'status': 'Молодец'}, answer)

if __name__ == "__main__":
    app.run(port=8000)
