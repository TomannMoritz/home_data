import os
from dotenv import load_dotenv

import miele_data

MIELE_API_TOKEN_ = "MIELE_API_TOKEN"


def query_miele():
    cwd = os.path.dirname(os.path.abspath(__file__)) + "/"
    miele_log_file = "miele.log"

    miele_data.setup(cwd, miele_log_file, "")

    miele_api_token = os.getenv(MIELE_API_TOKEN_)
    miele_data.query_device_information(miele_api_token)


def main():
    print("START")

    login_name = os.getlogin()
    load_dotenv(f"/home/{login_name}/.config/.env")

    query_miele()


if __name__ == "__main__":
    main()
