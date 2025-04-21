from time import gmtime, strftime, time

HOURS_AHEAD = 0
MINUTES_A_HOUR = 60
SECONDS_A_MINUTE = 60


def get_current_time():
    curr_time = time() + HOURS_AHEAD * MINUTES_A_HOUR * SECONDS_A_MINUTE
    return strftime("%Y-%m-%d %H:%M:%S", gmtime(curr_time))


def get_forecast_file_path():
    return strftime("%Y_%m_%d", gmtime())


def get_current_file_path():
    return strftime("%Y_%m", gmtime())
