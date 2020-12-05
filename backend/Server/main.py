# from redis import Redis
import subprocess
import os
import time
import traceback


def main():
    current_path = os.getcwd()
    flask_app_path = os.path.join(current_path, 'Flask', 'app_listener.py')
    flask_app = subprocess.Popen("python {} ".format(flask_app_path))
    try:
        while True:
            flask_app.wait()
    except KeyboardInterrupt:
        print('backend caught abort signal!')
        return 0
    except Exception as e:
        print('backend caught an unknown exception!')
        print('--------- STACK TRACE ---------')
        traceback.print_stack(e)
        print('--------- EXITING ---------')
        return -1


if __name__ == "__main__":
    main()
