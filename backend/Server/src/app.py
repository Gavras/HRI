import os

import flask
from flask import Flask, request

from quiz_manager import QuizManager

# main Flask app
app = Flask(__name__)

# HRI quiz manager
manager = QuizManager()


@app.route('/')
def index():
    return create_response('index')


@app.route('/get_question', methods=['POST', 'GET'])
def get_question():
    if 'idx' not in request.args:
        return create_response('Must enter idx')
    try:
        idx = int(request.args.get('idx'))
    except ValueError:
        return create_response('idx must be an int')
    print(f'backend got get_question request! idx={idx}', flush=True)
    return create_response(manager.get_question(idx))


@app.route('/submit_answer', methods=['POST', 'GET'])
def submit_answer():
    if 'idx' not in request.args:
        return create_response('Must enter idx')
    try:
        idx = int(request.args.get('idx'))
    except ValueError:
        return create_response('idx must be an int')
    if 'answer' not in request.args:
        return create_response('Must enter answer')
    answer = request.args.get('answer')
    print(f'backend got submit_answer request! idx={idx} answer={answer}', flush=True)
    return create_response(manager.submit_answer(idx, answer))


@app.route('/get_hint', methods=['POST', 'GET'])
def get_hint():
    if 'idx' not in request.args:
        return create_response('Must enter idx')
    try:
        idx = int(request.args.get('idx'))
    except ValueError:
        return create_response('idx must be an int')
    print(f'backend got get_hint request! idx={idx}', flush=True)
    return create_response(manager.get_hint(idx))


def create_response(msg):
    msg = flask.jsonify(msg)
    resp = flask.make_response(msg)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


def flask_main():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', manager.server_port)))


if __name__ == '__main__':
    flask_main()
