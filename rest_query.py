import subprocess
import json

import file
import date_time

FILE_EXTENSION = ".json"


def execute_curl_query(curl_query, cwd, log_file):
    result = subprocess.run(curl_query, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    print(f"\nReturn code: {result.returncode}")

    if (result.returncode != 0):
        file.update_file(cwd, log_file, f"[-] {date_time.get_current_time()} {result.returncode}\n")
        return None

    response_data = json.loads(result.stdout)

    return response_data
