import os
from dotenv import load_dotenv

import miele_data
import tibber_data

import file
import date_time

MIELE_API_TOKEN_ = "MIELE_API_TOKEN"
TIBBER_API_TOKEN_ = "TIBBER_API_TOKEN"
CWD = ""


def query_miele():
    miele_log_file = "miele.log"
    miele_data.setup(CWD, miele_log_file, "")

    miele_api_token = os.getenv(MIELE_API_TOKEN_)
    result = miele_data.query_device_information(miele_api_token)

    if result is None:
        return False

    file.update_file(CWD, miele_log_file, f"[+] {date_time.get_current_time()} Data received\n")
    return True


def query_tibber():
    tibber_log_file = "tibber.log"
    tibber_data.setup(CWD, tibber_log_file, "")

    tibber_api_token = os.getenv(TIBBER_API_TOKEN_)
    result = tibber_data.query_device_information(tibber_api_token, tibber_data.get_query_price_info_today())

    if result is None:
        return False
    file.update_file(CWD, tibber_log_file, f"[+] {date_time.get_current_time()} Data received\n")
    return True


def main():
    global CWD
    CWD = os.path.dirname(os.path.abspath(__file__)) + "/"

    login_name = os.getlogin()
    load_dotenv(f"/home/{login_name}/.config/.env")

    # TODO: requery with exponential backoff
    miele_successfull = query_miele()
    print("-------")
    tibber_successfull = query_tibber()


if __name__ == "__main__":
    main()
