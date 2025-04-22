import os
from dotenv import load_dotenv
import json
import sys
import time

import api.miele_data as miele_data
import api.tibber_data as tibber_data
import util.file as file

TIBBER_DATA_FILE = "tibber.json"
MIELE_DATA_FILE = "miele.json"

CURR_WAITING_TIME = 10
NUM_QUERIES = 1

SAVE_DATA_DIR = ""
LOG_DIR = ""


def setup():
    login_name = os.getlogin()
    load_dotenv(f"/home/{login_name}/.config/.env")

    global LOG_DIR, SAVE_DATA_DIR
    cwd = os.path.dirname(os.path.abspath(__file__)) + "/"
    LOG_DIR = cwd + "log/"
    SAVE_DATA_DIR = os.getenv("SAVE_DATA_DIR")


# -------------------------------------------------- #
def miele_get_device_info():
    result = miele_data.query_device_information()

    if result is None:
        return False

    file.data_received(LOG_DIR, miele_data.LOG_FILE)
    file.overwrite_file(SAVE_DATA_DIR, MIELE_DATA_FILE, json.dumps(result))

    return True


def miele_start_devices():
    miele_device_data = file.get_json_data(SAVE_DATA_DIR, MIELE_DATA_FILE)
    device_ids = miele_data.get_ids(miele_device_data)

    for device_id in device_ids:
        miele_start_device(device_id)


def miele_start_device(device_id):
    miele_device_data = file.get_json_data(SAVE_DATA_DIR, MIELE_DATA_FILE)

    status = miele_data.get_status(miele_device_data)
    ids = miele_data.get_ids(miele_device_data)

    if device_id not in ids:
        return

    device_status = status[ids.index(device_id)]

    # Device is OFF
    if device_status == 1:
        file.msg(LOG_DIR, miele_data.LOG_FILE, "[~]", f"ID: {device_id} IS OFF")
        return

    res = miele_data.execute_action(device_id, "START")

    if res:
        file.msg(LOG_DIR, miele_data.LOG_FILE, "[*]", f"ID: {device_id} STARTED")
        return
    file.msg(LOG_DIR, miele_data.LOG_FILE, "[~]", f"ID: {device_id} COULD NOT BE STARTED")


# -------------------------------------------------- #
def tibber_get_energy_prices():
    result = tibber_data.query_device_information(tibber_data.get_query_price_info_today())

    if result is None:
        return False

    file.data_received(LOG_DIR, tibber_data.LOG_FILE)
    file.overwrite_file(SAVE_DATA_DIR, TIBBER_DATA_FILE, json.dumps(result))
    return True


# -------------------------------------------------- #
def exponential_backoff(fn, log_file):
    global CURR_WAITING_TIME, NUM_QUERIES
    CURR_WAITING_TIME *= 2
    NUM_QUERIES += 1

    if NUM_QUERIES > 4:
        file.msg(LOG_DIR, log_file, "[!]", f" COULD NOT GET DATA - WAITING TIME: {CURR_WAITING_TIME} - QUERIES: {NUM_QUERIES}")
        return

    success = fn()
    if not success:
        time.sleep(CURR_WAITING_TIME)
        exponential_backoff(fn, log_file)


def main():
    setup()

    if len(sys.argv) <= 2:
        print("[!] NOT ENOUGH ARGUMENTS")
        return

    if sys.argv[1] == "miele":
        miele_data.setup(LOG_DIR, "miele.log", "")

        if sys.argv[2] == "get_device_info":
            exponential_backoff(miele_get_device_info, miele_data.LOG_FILE)

        if sys.argv[2] == "start_devices":
            miele_start_devices()

        if sys.argv[2] == "start_device" and len(sys.argv) == 4:
            miele_start_device(sys.argv[3])
        return

    if sys.argv[1] == "tibber":
        tibber_data.setup(LOG_DIR, "tibber.log", "")

        if sys.argv[2] == "get_energy_prices":
            exponential_backoff(tibber_get_energy_prices, tibber_data.LOG_FILE)
        return


if __name__ == "__main__":
    main()
