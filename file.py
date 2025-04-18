import os

import date_time


def update_dir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def update_file(dir_path, file_path, data):
    update_dir(dir_path)
    if not os.path.isfile(dir_path + file_path):
        with open(file_path, "w") as f:
            f.write(data)
            return

    with open(file_path, "a") as f:
        f.write(data)


def overwrite_file(dir_path, file_path, data):
    update_dir(dir_path)
    with open(dir_path + file_path, "w") as f:
        f.write(data)


# -------------------------------------------------- #
def api_token_missing(dir_path, file_path):
    update_file(dir_path, file_path, f"[!] {date_time.get_current_time()} API TOKEN MISSING\n")


def api_url_missing(dir_path, file_path):
    update_file(dir_path, file_path, f"[!] {date_time.get_current_time()} API URL MISSING\n")


def data_received(dir_path, file_path):
    update_file(dir_path, file_path, f"[+] {date_time.get_current_time()} Data received\n")
