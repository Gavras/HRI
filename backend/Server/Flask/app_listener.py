import flask
from flask import Flask, request
from quiz_manager import QuizManager

# main Flask app
app = Flask(__name__)

# HRI quiz manager
manager = QuizManager()


@app.route('/get_question', methods=['POST', 'GET'])
def get_question():
    print('backend got get_question request!')
    return create_response(manager.get_question())


@app.route('/submit_answer', methods=['POST', 'GET'])
def submit_answer():
    answer = request.args.get('answer')
    print(f'backend got submit_answer request! answer={answer}')
    return create_response(manager.submit_answer(answer))


@app.route('/get_hint', methods=['POST', 'GET'])
def get_hint():
    print('backend got get_hint request!')
    return create_response(manager.get_hint())

def create_response(msg):
    resp = flask.make_response(msg)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

def flask_main():
    app.run(host='0.0.0.0', port=manager.backend_port)


if __name__ == '__main__':
    flask_main()
