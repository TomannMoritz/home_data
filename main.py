import os
from dotenv import load_dotenv
import json

import api.miele_data as miele_data
import api.tibber_data as tibber_data
import util.file as file

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


def miele_get_device_info():
    result = miele_data.query_device_information()

    if result is None:
        return False

    file.data_received(LOG_DIR, miele_data.LOG_FILE)
    file.overwrite_file(SAVE_DATA_DIR, MIELE_DATA_FILE, json.dumps(result))

    return True


def miele_start_devices():
    miele_device_data = file.get_json_data(SAVE_DATA_DIR, MIELE_DATA_FILE)

    for device in miele_device_data:
        device_id = device["fabNumber"]
        res = miele_data.execute_action(device_id, "START")
        print(res)


def query_tibber():
    result = tibber_data.query_device_information(tibber_data.get_query_price_info_today())

    if result is None:
        return False

    file.data_received(LOG_DIR, tibber_data.LOG_FILE)
    file.overwrite_file(SAVE_DATA_DIR, TIBBER_DATA_FILE, json.dumps(result))
    return True


def main():
    setup()

    # TODO: requery with exponential backoff
    miele_data.setup(LOG_DIR, "miele.log", "")
    miele_successfull = miele_get_device_info()
    miele_start_devices()

    print("-------")
    tibber_data.setup(LOG_DIR, "tibber.log", "")
    tibber_successfull = query_tibber()


if __name__ == "__main__":
    main()
