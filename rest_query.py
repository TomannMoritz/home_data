import subprocess
import json

import file
import date_time

FILE_EXTENSION = ".json"


def set_environment(api_token, api_url, cwd, log_file="no_file.log"):
    if api_token is None or not api_token:
        file.api_token_missing(cwd, log_file)
        return False

    if api_url is None or not api_url:
        file.api_url_missing(cwd, log_file)
        return False
    return True


def execute_curl_query(curl_query, cwd, log_file):
    result = subprocess.run(curl_query, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    print(f"\nReturn code: {result.returncode}")

    if (result.returncode != 0):
        file.update_file(cwd, log_file, f"[-] {date_time.get_current_time()} {result.returncode}\n")
        return None

    response_data = json.loads(result.stdout)

    return response_data
