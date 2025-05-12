import os
import json

import util.rest_query as rest_query
import util.file as file


CWD = ""
LOG_FILE = ""
MIELE_URL = "https://api.mcs3.miele.com/v1"
MIELE_API_TOKEN_ = "MIELE_API_TOKEN"
API_TOKEN = ""

DEVICE_ACTIONS = {
        "START": 1,
        "STOP": 2,
        "PAUSE": 3
        }

DEVICE_STATE = {
        "OFF": 1,
        "ON": 2,
        "PROGRAMMED": 3,
        "PROGRAMMED WAITING TO START": 4,
        "RUNNING": 5,
        "PAUSE": 6,
        "END PROGRAMMED": 7,
        }


def setup(cwd, log_file, api_url):
    global CWD, LOG_FILE, MIELE_URL, API_TOKEN
    CWD = cwd
    LOG_FILE = log_file
    API_TOKEN = os.getenv(MIELE_API_TOKEN_)

    if api_url is not None and api_url != "":
        MIELE_URL = api_url


def query_device_information(language="en"):
    if not rest_query.set_environment(API_TOKEN, MIELE_URL, CWD, LOG_FILE):
        return

    # Request data
    curl_command = ["curl",
                    "-X", "GET",
                    f"{MIELE_URL}/devices?language={language}",
                    "-H",  f"Authorization: Bearer {API_TOKEN}",
                    "-H", "accept: application/json; charset=utf-8"
                    ]

    result = rest_query.execute_curl_query(curl_command, CWD, LOG_FILE)

    for id, device_type in zip(get_ids(result), get_device_types(result)):
        print(f"Device: {device_type} - ID: {id}")

    return result


def execute_action(device_id, action):
    actions = get_available_actions(device_id)

    if DEVICE_ACTIONS[action] not in actions:
        file.msg(CWD, LOG_FILE, "[~]", f"ID: {device_id} ACTION: <{action}> NOT AVAILABLE")
        return False

    query_data = json.dumps({"processAction": DEVICE_ACTIONS[action]})
    curl_command = ["curl",
                    "-X", "PUT",
                    f"{MIELE_URL}/devices/{device_id}/actions",
                    "-H",  f"Authorization: Bearer {API_TOKEN}",
                    "-H", "Content-Type: application/json",
                    "-d", query_data
                    ]

    result = rest_query.execute_curl_query(curl_command, CWD, LOG_FILE)
    print(result)
    file.msg(CWD, LOG_FILE, "[*]", f"ID: {device_id} ACTION: <{action}> EXECUTED")
    return True


def get_available_actions(device_id):
    # Request data
    curl_command = ["curl",
                    "-X", "GET",
                    f"{MIELE_URL}/devices/{device_id}/actions",
                    "-H",  f"Authorization: Bearer {API_TOKEN}",
                    "-H", "accept: application/json; charset=utf-8"
                    ]

    result = rest_query.execute_curl_query(curl_command, CWD, LOG_FILE)
    return result["processAction"]


def get_ids(device_info):
    return [key for key in device_info.keys()]


def get_device_types(device_info):
    device_types = []
    for key in device_info.keys():
        entry = device_info[key]["ident"]
        device_type = entry["type"]["value_localized"]
        device_types.append(device_type)
    return device_types


def get_start_times(device_info):
    device_start_times = []
    for key in device_info.keys():
        entry = device_info[key]["state"]
        device_time = entry["startTime"]
        device_start_times.append(device_time)
    return device_start_times


def get_status(device_info):
    device_status = []
    for key in device_info.keys():
        entry = device_info[key]["state"]
        curr_status = entry["status"]["value_raw"]
        device_status.append(curr_status)
    return device_status


def get_program_ids(device_info):
    program_ids = []
    for key in device_info.keys():
        entry = device_info[key]["state"]
        program_id = entry["ProgramID"]["value_raw"]
        program_ids.append(program_id)
    return program_ids


# --------------------------------------------------
# Device Status

def skip_device(device_state, device_id):
    if device_is_off(device_state):
        return True, ["[~]", f"DEVICE: {device_id} IS OFF"]

    if device_is_running(device_state):
        return True, ["[~]", f"DEVICE: {device_id} IS RUNNING"]

    if device_finished(device_state):
        return True, ["[~]", f"DEVICE: {device_id} FINISHED"]

    if not device_is_waiting_to_start(device_state):
        return True, ["[~]", f"DEVICE: {device_id} SKIPPED - STATUS: {device_state}"]
    return False, []


def device_is_off(device_state):
    return device_state == DEVICE_STATE["OFF"]


def device_is_running(device_state):
    return device_state == DEVICE_STATE["RUNNING"]


def device_is_waiting_to_start(device_state):
    return device_state == DEVICE_STATE["PROGRAMMED WAITING TO START"]


def device_finished(device_state):
    return device_state == DEVICE_STATE["END PROGRAMMED"]

