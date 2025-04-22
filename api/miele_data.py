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
                    f"{MIELE_URL}/short/devices?language={language}",
                    "-H",  f"Authorization: Bearer {API_TOKEN}",
                    "-H", "accept: application/json; charset=utf-8"
                    ]

    result = rest_query.execute_curl_query(curl_command, CWD, LOG_FILE)

    for entry in result:
        print(f"Device: {entry['type']} - ID: {entry['fabNumber']}")

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
