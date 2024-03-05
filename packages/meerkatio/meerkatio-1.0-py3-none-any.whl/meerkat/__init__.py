import os
import time
from playsound import playsound

from meerkat.api import send_meerkat_notification, get_user_token

module_runtime = int(time.time()*1000)

if not os.environ.get("MEERKAT_TOKEN"):
    try:
        with open(os.path.expanduser("~") + "/.meerkat") as file:
            os.environ["MEERKAT_TOKEN"] = file.read()
    except Exception as e:
        print(e)
        pass

#
# User Management Functions
#
def login(email: str, password: str) -> bool:
    token = get_user_token(email, password)

    if not token:
        print("Invalid Meerkat Token!")
        return False

    os.environ["MEERKAT_TOKEN"] = token
    return True

#
# Notification Functions
#
def ping():
    ping_file_path = "/ping_sounds/default_ping.mp3"
    playsound(os.path.abspath(os.path.dirname(__file__)) + ping_file_path)

def email(token=None, message=""):
    if token == None:
        token = os.environ.get("MEERKAT_TOKEN")

    if not token:
        return
    
    return send_meerkat_notification("email", token, message)