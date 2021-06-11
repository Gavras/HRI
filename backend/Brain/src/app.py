import argparse
import random
import socket
import time

from naoqi import ALProxy

nao_robot_ip = '1.1.1.1'
nao_robot_port = 9559

brain_port = 9000

correct_behaviors = [
    'Behaviors/correct1A',
    'Behaviors/correct1B',
    'Behaviors/correct1C',
    'Behaviors/correct2A',
    'Behaviors/correct2B',
    'Behaviors/correct2C',
    'Behaviors/correct3A',
    'Behaviors/correct3B',
    'Behaviors/correct3C',
    'Behaviors/correct4A',
    'Behaviors/correct4B',
    'Behaviors/correct4C',
]

incorrect_behaviors = [
    'Behaviors/incorrect1A',
    'Behaviors/incorrect1B',
    'Behaviors/incorrect2A',
    'Behaviors/incorrect2B',
    'Behaviors/incorrect3A',
    'Behaviors/incorrect3B',
]


class NaoRobot:

    def __init__(self, robot_ip='127.0.0.1', robot_port=9559):
        self.ip = robot_ip
        self.port = robot_port

        self.behavior = ALProxy('ALBehaviorManager', self.ip, self.port)
        self.speech = ALProxy('ALTextToSpeech', self.ip, self.port)
        self.motion = ALProxy('ALMotion', self.ip, self.port)
        self.posture = ALProxy('ALRobotPosture', self.ip, self.port)

        time.sleep(1)

    def runBEHAVIOR(self, behaviorPath):
        self.behavior.runBehavior(behaviorPath)

    def runDefaultPosture(self, posture, speed=1.0):
        """
        those are predefined postures
        you should pass one of those to the function as string:
        Crouch,
        LyingBack,
        LyingBelly,
        Sit,
        SitRelax,
        Stand,
        StandInit,
        StandZero
        """
        self.posture.goToPosture(posture, speed)

    def runSPEECH(self, text):
        self.speech.say(text)


def main():
    args = get_args()
    robot_ip = '127.0.0.1' if args.local else nao_robot_ip
    nao = NaoRobot(robot_ip=robot_ip, robot_port=nao_robot_port)
    brain_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    brain_socket.bind(('0.0.0.0', brain_port))
    brain_socket.listen(1)

    while True:
        server, _ = brain_socket.accept()
        msg = server.recv(1024)
        print('Brain got message ', msg)
        if msg.startswith('start:'):
#             nao.runBEHAVIOR('Behaviors/welcome')
            name = msg[len('start:'):]
            text = 'hello ' + name
            nao.runSPEECH(text)
        elif msg == 'end':
            nao.runBEHAVIOR('Behaviors/good_bye')
        elif msg == 'true':
            nao.runBEHAVIOR(random.choice(correct_behaviors))
        elif msg == 'false':
            nao.runBEHAVIOR(random.choice(incorrect_behaviors))
        elif msg.startswith('hint:'):
            nao.runBEHAVIOR('hint')
            hint = msg[len('hint:'):]
            nao.runSPEECH(hint)
        else:
            print('Brain got unknown msg ', msg)
            continue
        answer = 'Brain accepted msg ' + msg
        server.send(bytes(answer))


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--local', action='store_true')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    main()
