import os
import json

import util.date_time as date_time


def update_dir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def update_file(dir_path, file_path, data):
    update_dir(dir_path)
    if not os.path.isfile(dir_path + file_path):
        with open(dir_path + file_path, "w") as f:
            f.write(data)
            return

    with open(dir_path + file_path, "a") as f:
        f.write(data)


def overwrite_file(dir_path, file_path, data):
    update_dir(dir_path)
    with open(dir_path + file_path, "w") as f:
        f.write(str(data))


def get_json_data(dir_path, file_path):
    if not os.path.isfile(dir_path + file_path):
        return None
    with open(dir_path + file_path, "r") as f:
        return json.load(f)


# -------------------------------------------------- #
def api_token_missing(dir_path, file_path):
    update_file(dir_path, file_path, f"[!] {date_time.get_current_time()} API TOKEN MISSING\n")


def api_url_missing(dir_path, file_path):
    update_file(dir_path, file_path, f"[!] {date_time.get_current_time()} API URL MISSING\n")


def data_received(dir_path, file_path):
    update_file(dir_path, file_path, f"[+] {date_time.get_current_time()} Data received\n")


def msg(dir_path, file_path, msg_level, msg):
    update_file(dir_path, file_path, f"{msg_level} {date_time.get_current_time()} {msg}\n")
