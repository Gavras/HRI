import json
import os
from configparser import ConfigParser
import logging
import socket

# os.environ['QUIZ_MANAGER_NO_BRAIN'] = '1'
from threading import Thread


class QuizManager:
    def __init__(self):
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        config_file_path = os.path.join(cur_dir, 'config.ini')
        config = ConfigParser()
        config.read(config_file_path)
        app_config = config['config']

        self.brain_ip = app_config['brain_ip']
        self.brain_port = int(app_config['brain_port'])
        self.server_port = app_config.getint('server_port')

        config_quiz_file_path = app_config['quiz_file_path']
        if os.path.isabs(config_quiz_file_path):
            quiz_file_path = config_quiz_file_path
        else:
            quiz_file_path = os.path.abspath(os.path.join(os.path.dirname(config_file_path), config_quiz_file_path))
        self.questions, self.possible_answers, self.correct_answers, self.hints, \
        self.positive_responses, self.negative_responses = self.parse_quiz(quiz_file_path)

        self.current_question_idx = len(self.questions) - 1
        self.question_number = 1
        self.log_path = os.path.join(os.path.dirname(quiz_file_path), 'user_actions.log')
        self.logger = self.get_logger()
        with open(self.log_path, 'w'):
            pass

    def send_to_brain(self, msg):
        if 'QUIZ_MANAGER_NO_BRAIN' in os.environ:
            return

        def send_to_brain_t():
            brain_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                brain_socket.settimeout(1)
                brain_socket.connect((self.brain_ip, self.brain_port))
                brain_socket.send(bytes(msg, 'utf-8'))
            except socket.timeout:
                pass
            finally:
                brain_socket.close()

        thread = Thread(target=send_to_brain_t)
        thread.start()

    def get_logger(self):
        new_logger = logging.getLogger(__name__)
        new_logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)-8s %(message)s', '%Y-%m-%d %H:%M:%S')
        file_handler = logging.FileHandler(self.log_path)
        file_handler.setFormatter(formatter)
        new_logger.addHandler(file_handler)
        return new_logger

    def log_action(self, message):
        self.logger.info(message)

    def get_question(self, idx):
        if idx == 0:
            self.send_to_brain('start')
        if idx is not None:
            self.current_question_idx = int(idx)
            self.question_number = int(idx)
        else:
            self.current_question_idx = (self.current_question_idx + 1) % len(self.questions)
        if self.question_number == len(self.questions):
            question = {'question': 'No More Questions!',
                        'possible_answers': []}
        else:
            question = {'question': self.questions[self.current_question_idx],
                        'possible_answers': self.possible_answers[self.current_question_idx]}
            self.question_number += 1
        return question

    def check_answer(self, answer):
        return self.correct_answers[self.current_question_idx] == answer

    def submit_answer(self, answer):
        if self.check_answer(answer):
            self.send_to_brain('true')
            response = {'answer': 'correct',
                        'response': self.positive_responses[self.current_question_idx]}
        else:
            self.send_to_brain('false')
            response = {'answer': 'incorrect',
                        'response': self.negative_responses[self.current_question_idx]}

        return response

    def get_hint(self):
        self.send_to_brain('hint')
        return self.hints[self.current_question_idx]

    @staticmethod
    def parse_quiz(quiz_file_path):
        questions = []
        possible_answers = []
        correct_answers = []
        hints = []
        positive_responses = []
        negative_responses = []

        with open(quiz_file_path, 'r') as quiz_file:
            data = quiz_file.read()
        quiz_data = json.loads(data)

        for question_key in quiz_data:
            quiz_question = quiz_data[question_key]
            questions.append(quiz_question["question"])
            possible_answers.append(quiz_question["possible_answers"])
            correct_answers.append(quiz_question["correct_answer"])
            hints.append(quiz_question["hint"])
            positive_responses.append(quiz_question["positive_response"])
            negative_responses.append(quiz_question["negative_response"])

        return questions, possible_answers, correct_answers, hints, positive_responses, negative_responses
