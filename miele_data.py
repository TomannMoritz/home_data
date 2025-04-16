import rest_query
import file
import date_time

CWD = ""
LOG_FILE = ""
MIELE_URL = "https://api.mcs3.miele.com/v1/short/devices?language=de"


def setup(cwd, log_file, api_url):
    global CWD, LOG_FILE, MIELE_URL
    CWD = cwd
    LOG_FILE = log_file
    if api_url is not None and api_url != "":
        MIELE_URL = api_url


def query_device_information(api_token):
    if api_token is None or not api_token:
        file.update_file(CWD, LOG_FILE, f"[!] {date_time.get_current_time()} API TOKEN MISSING\n")
        return

    if MIELE_URL is None or not MIELE_URL:
        file.update_file(CWD, LOG_FILE, f"[!] {date_time.get_current_time()} API URL MISSING\n")
        return

    # Request data
    curl_command = ["curl",
                    "-X", "GET",
                    MIELE_URL,
                    "-H",  f"Authorization: Bearer {api_token}",
                    "-H", "accept: application/json; charset=utf-8"
                    ]

    result = rest_query.execute_curl_query(curl_command, CWD, LOG_FILE)

    for entry in result:
        print(f"Device: {entry['type']} - ID: {entry['fabNumber']}")

    return result

