from flask import Flask, request
from quiz_manager import QuizManager

# main Flask app
app = Flask(__name__)

# HRI quiz manager
manager = QuizManager()


@app.route('/get_question', methods=['POST', 'GET'])
def get_question():
    print('backend got get_question request!')
    return manager.get_question()


@app.route('/next_question', methods=['POST', 'GET'])
def next_question():
    print('backend got next_question request!')
    manager.next_question()
    return "Next question is now active!"


@app.route('/submit_answer', methods=['POST', 'GET'])
def submit_answer():
    answer = request.form.get('answer')
    print('backend got submit_answer request!')
    return manager.submit_answer(answer)


@app.route('/get_hint', methods=['POST', 'GET'])
def get_hint():
    print('backend got get_hint request!')
    return manager.get_hint()


def flask_main():
    app.run(host='0.0.0.0', port=manager.backend_port)


if __name__ == '__main__':
    flask_main()
