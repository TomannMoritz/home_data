import os
from dotenv import load_dotenv


TIBBER_DATA_FILE = "tibber.json"
MIELE_DATA_FILE = "miele.json"


SAVE_DATA_DIR = ""
LOG_DIR = ""


def setup():
    login_name = os.getlogin()
    load_dotenv(f"/home/{login_name}/.config/.env")

    global LOG_DIR, SAVE_DATA_DIR
    cwd = os.path.dirname(os.path.abspath(__file__)) + "/"
    LOG_DIR = cwd + "log/"
    SAVE_DATA_DIR = os.getenv("SAVE_DATA_DIR")
