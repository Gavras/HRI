import base64
import json
import os
from configparser import ConfigParser
import logging


class QuizManager:
    def __init__(self):
        # read and extract config from file to a dictionary of parameters
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        config_file_path = os.path.join(cur_dir, 'config.ini')
        config = ConfigParser()
        config.read(config_file_path)
        app_config = config['config']

        # Network configs
        self.nao_ip = app_config['nao_ip']
        self.nao_port = app_config.getint('nao_port')
        self.app_port = app_config.getint('app_port')
        self.backend_port = app_config.getint('backend_port')

        # Quiz config
        config_quiz_file_path = app_config['quiz_file_path']
        if os.path.isabs(config_quiz_file_path):
            quiz_file_path = config_quiz_file_path
        else:
            quiz_file_path = os.path.abspath(os.path.join(os.path.dirname(config_file_path), config_quiz_file_path))
        self.questions, self.possible_answers, self.correct_answers, self.hints, \
            self.positive_responses, self.negative_responses = self.parse_quiz(quiz_file_path)

        self.nao_gifs_dir = os.path.abspath(os.path.join(cur_dir, '..', 'gifs'))

        self.current_question_idx = len(self.questions) - 1
        self.question_number = 1
        self.logger = self.get_logger()
        with open('user_actions.log', 'w'):
            pass

    @staticmethod
    def get_logger():
        new_logger = logging.getLogger(__name__)
        new_logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)-8s %(message)s', '%Y-%m-%d %H:%M:%S')
        file_handler = logging.FileHandler('user_actions.log')
        file_handler.setFormatter(formatter)
        new_logger.addHandler(file_handler)
        return new_logger

    def log_action(self, message):
        self.logger.info(message)

    def get_gif_string(self, gif_name):
        gif = os.path.join(self.nao_gifs_dir, f'{gif_name}.gif')
        with open(gif, 'rb') as gif_file:
            r = base64.b64encode(gif_file.read()).decode('ascii')
        return r

    def get_gif(self, gif):
        return self.get_gif_string(gif)

    # return current question
    def get_question(self, idx):
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

    # check if submitted answer is in-fact the correct answer
    def check_answer(self, answer):
        # check if the answer provided matches the correct answer
        return self.correct_answers[self.current_question_idx] == answer

    # submit answer and return response based on success
    def submit_answer(self, answer):
        # extract correct response and move to next question if the answer is correct
        if self.check_answer(answer):
            response = {'answer': 'correct',
                        'response': self.positive_responses[self.current_question_idx],
                        'gif': self.get_gif_string('correct_answer')}
        else:
            response = {'answer': 'incorrect',
                        'response': self.negative_responses[self.current_question_idx],
                        'gif': self.get_gif_string('incorrect_answer')}

        return response

    # return current hint
    def get_hint(self):
        return self.hints[self.current_question_idx]

    # parse the quiz json file
    @staticmethod
    def parse_quiz(quiz_file_path):
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
