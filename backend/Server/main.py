import subprocess
import os
import sys
import time
import traceback


def main():
    current_path = os.path.dirname(os.path.abspath(__file__))
    flask_app_path = os.path.join(current_path, 'Flask', 'app_listener.py')
    # open a subprocess to run the flask app listener
    print(f'Running command "{sys.executable}" "{flask_app_path}"')
    flask_app = subprocess.Popen(f'"{sys.executable}" "{flask_app_path}"', shell=True)
    try:
        # add more logic/workers here

        # this line will block and wait for the flask_app to finish.
        # add this wait() method to every subprocess opened for clean exit.
        flask_app.wait()
    except KeyboardInterrupt:
        print('backend caught abort signal!')
        return 0
    except Exception as e:
        # print stacktrace for unknown exceptions. Handle all known exceptions before this clause
        print('backend caught an unknown exception!')
        print('--------- STACK TRACE ---------')
        traceback.print_stack(e)
        print('--------- EXITING ---------')
        return -1


if __name__ == "__main__":
    main()
