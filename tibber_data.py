import json
import os

import rest_query
import file


CWD = ""
LOG_FILE = ""
TIBBER_URL = "https://api.tibber.com/v1-beta/gql"
TIBBER_API_TOKEN_ = "TIBBER_API_TOKEN"
API_TOKEN = ""


def setup(cwd, log_file, api_url):
    global CWD, LOG_FILE, TIBBER_URL, API_TOKEN
    CWD = cwd
    LOG_FILE = log_file
    API_TOKEN = os.getenv(TIBBER_API_TOKEN_)

    if api_url is not None and api_url != "":
        TIBBER_URL = api_url


def get_query_price_info_today():
    return """ {
            viewer {
                homes {
                    currentSubscription {
                        priceInfo {
                            today {
                                total
                                startsAt
                                }
                            }
                        }
                    }
                }
            }
    """


def get_extracted_data(tibber_data, day="today"):
    data_today = tibber_data["data"]["viewer"]["homes"][0]["currentSubscription"]["priceInfo"][day]
    return data_today


def get_price_array(extracted_data):
    return [price["total"] for price in extracted_data]


def query_device_information(price_info_query):
    if API_TOKEN is None or not API_TOKEN:
        file.api_token_missing(CWD, LOG_FILE)
        return

    if TIBBER_URL is None or not TIBBER_URL:
        file.api_url_missing(CWD, LOG_FILE)
        return

    query_body = json.dumps({"query": price_info_query})

    # Request data
    curl_command = ["curl",
                    "-X", "POST",
                    TIBBER_URL,
                    "-H",  f"Authorization: Bearer {API_TOKEN}",
                    "-H", "Content-Type: application/json",
                    "-d", query_body
                    ]

    result = rest_query.execute_curl_query(curl_command, CWD, LOG_FILE)

    data_today = get_extracted_data(result)
    return data_today


