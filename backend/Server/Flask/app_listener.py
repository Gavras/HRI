from flask import Flask, request
from redis import Redis
import json
import os
from configparser import ConfigParser


class HRIManager:
    def __init__(self):
        # read and extract config from file to a dictionary of parameters
        config_file_path = os.path.join('C:\\', 'Users', 'razda', 'Desktop', 'HRI', 'backend', 'Server', 'Flask', 'config.ini')
        config = ConfigParser()
        config.read(config_file_path)
        app_config = config['config']

        self.nao_ip = app_config['nao_ip']
        self.nao_port = app_config.getint('nao_port')
        self.app_port = app_config.getint('app_port')
        self.backend_port = app_config.getint('backend_port')
        quiz_file_path = app_config['quiz_file_path']
        # generate a dictionary of questions
        self.questions, self.possible_answers, self.correct_answers, self.hints, \
            self.positive_responses, self.negative_responses = self.parse_quiz(quiz_file_path)
        self.current_question_idx = 0

    def parse_quiz(self, quiz_file_path):
        questions = []
        possible_answers = []
        correct_answers = []
        hints = []
        positive_responses = []
        negative_responses = []

        # parse data from quiz JSON file
        with open(quiz_file_path, 'r') as quiz_file:
            data = quiz_file.read()
        quiz_data = json.loads(data)

        # extract the data from parsed JSON quiz
        for question_key in quiz_data:
            quiz_question = quiz_data[question_key]
            questions.append(quiz_question["question"])
            possible_answers.append(quiz_question["possible_answers"])
            correct_answers.append(quiz_question["correct_answer"])
            hints.append(quiz_question["hint"])
            positive_responses.append(quiz_question["positive_response"])
            negative_responses.append(quiz_question["negative_response"])

        return questions, possible_answers, correct_answers, hints, positive_responses, negative_responses

    def get_question(self):
        question = {'question': self.questions[self.current_question_idx],
                    'possible_answers': self.possible_answers[self.current_question_idx]}
        return json.dumps(question)

    def check_answer(self, answer):
        # check if the answer stored at the index pointed by correct_answers[question_idx] matches given answer
        return self.possible_answers[self.correct_answers[self.current_question_idx]] == answer

    def submit_answer(self, answer):
        # extract correct response and move to next question if the answer is correct
        if self.check_answer(answer):
            response = self.positive_responses[self.current_question_idx]
            self.current_question_idx += 1
        else:
            response = self.negative_responses[self.current_question_idx]

        return json.dumps({'response': json.dumps(response)})

    def get_hint(self):
        return json.dumps({'hint': json.dumps(self.hints[self.current_question_idx])})


app = Flask(__name__)
manager = HRIManager()


@app.route('/get_question', methods=['POST', 'GET'])
def get_question():
    return manager.get_question()


@app.route('/submit_answer', methods=['POST', 'GET'])
def submit_answer():
    return manager.submit_answer(request.json)


@app.route('/get_hint', methods=['POST', 'GET'])
def get_hint():
    return manager.get_hint()


def flask_main():
    app.run(host='0.0.0.0', port=manager.backend_port)


if __name__ == '__main__':
    flask_main()
