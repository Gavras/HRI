import time
import json
import socket
from datetime import datetime


class Nao_Robot_wrapper_36:
    def __init__(self, ip="127.0.0.1", port=8001):
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET)
        self.socket = socket.create_connection((self.ip, self.port))

    def runBEHAVIOR(self, behavior):
        # Send behavior path over socket
        self.socket.send(json.dumps({'action': 'behavior', 'behavior': behavior,
                                     'time': datetime.utcnow().timestamp()}))

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
        # Send posture and speed over socket
        self.socket.send(json.dumps({'action': 'posture', 'posture': posture, 'speed': speed,
                                     'time': datetime.utcnow().timestamp()}))

    def runSPEECH(self, text):
        # Send speech over socket
        self.socket.send(json.dumps({'action': 'speech', 'text': text,
                                     'time': datetime.utcnow().timestamp()}))
