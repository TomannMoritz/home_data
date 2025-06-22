import os
from dotenv import load_dotenv


TIBBER_DATA_FILE = "tibber.json"
MIELE_DATA_FILE = "miele.json"

ENVIRONMENT_FILE_PATH = ""


SAVE_DATA_DIR = ""
LOG_DIR = ""


def setup():
    global ENVIRONMENT_FILE_PATH
    login_name = os.getlogin()
    ENVIRONMENT_FILE_PATH = f"/home/{login_name}/.config/.env"
    load_dotenv(ENVIRONMENT_FILE_PATH)

    global LOG_DIR, SAVE_DATA_DIR
    cwd = os.path.dirname(os.path.abspath(__file__)) + "/"
    LOG_DIR = cwd + "log/"
    SAVE_DATA_DIR = os.getenv("SAVE_DATA_DIR")


def update_entry(key, value):
    lines = []
    # get environment file data
    with open(ENVIRONMENT_FILE_PATH, "r") as f:
        for line in f:
            if key + "=" in line:
                lines.append(key + "=" + value + "\n")
                continue
            lines.append(line)

    # update environment file
    with open(ENVIRONMENT_FILE_PATH, "w") as f:
        f.writelines(lines)

    return True

