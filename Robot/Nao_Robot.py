from naoqi import ALProxy, ALModule, ALBroker
import time
import json
import socket
import os

class Nao_Robot_27:
    def __init__(self, ip="127.0.0.1", backend_port=8002, robot_port=9559):
        self.ip = ip
        self.robot_port = robot_port
        self.backend_port = backend_port
        self.backend_socket = socket.socket(socket.AF_INET)
        self.backend_socket = self.backend_socket.create_connection(('0.0.0.0', self.backend_port))
        try:
            self.behavior = ALProxy("ALBehaviorManager", self.ip, self.robot_port)
            self.speech = ALProxy("ALTextToSpeech", self.ip, self.robot_port)
            self.motion = ALProxy("ALMotion", self.ip, self.robot_port)
            self.posture = ALProxy("ALRobotPosture", self.ip, self.robot_port)
        except Exception as e:
            print(e)
            raise e

    def runBEHAVIOR(self, behavior):
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        behaviors_dir = os.path.join(cur_dir, 'Behaviors')
        behavior_path = os.path.join(behaviors_dir, behavior)
        self.behavior.runBehavior(behavior_path)

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

    # Run forever wait for requests from the backend server
    def run_robot(self):
        while True:
            try:
                # Eliminate messages that are too old
                data = json.loads(self.backend_socket.recv(1024))
                if data['action'] == 'behavior':
                    self.runBEHAVIOR(data['behavior'])
                if data['action'] == 'posture':
                    self.runDefaultPosture(data['posture'], data['speed'])
                if data['action'] == 'speech':
                    self.runSPEECH(data['text'])
                # Do not allow consecutive requests to arrive too quickly
                time.sleep(2)
            except Exception as e:
                # Something bad happened - reconnect to robot and continue loop
                print(e)

if __name__ == "__main__":
    robot = Nao_Robot_27()
    robot.run_robot()
