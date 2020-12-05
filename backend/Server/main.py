from redis import Redis
import subprocess
import os
import time
import traceback


def main():
    flask_app_path = os.path.join('backend', 'Server', 'Flask', 'app_listener.py')
    flask = subprocess.Popen("python3 {} ".format(flask_app_path))
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('backend caught abort signal!')
        return 0
    except Exception as e:
        print('backend caught an unknown exception!')
        print('--------- STACK TRACE ---------')
        traceback.print_stack(e)
        print('--------- EXITING ---------')
        return -1

