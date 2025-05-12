from time import localtime, strftime


def get_current_time():
    return strftime("%Y-%m-%d %H:%M:%S", localtime())


def get_hour_minute():
    return int(strftime("%H", localtime())), int(strftime("%M", localtime()))


def get_next_quarter(curr_hour, curr_minute):
    assert curr_hour < 24, f"Invalid input: {curr_hour=}"
    assert curr_minute < 60, f"Invalid input: {curr_minute=}"

    remaining = 15 - (curr_minute % 15)
    minute = curr_minute + remaining

    if minute >= 60:
        return (curr_hour + 1) % 24, 0
    return curr_hour, minute


def get_index_quarter(hour, minute):
    return 4 * hour + int(minute // 15)


def get_quarter_time(index):
    hour = (index // 4) % 24
    minute = 15 * (index % 4)
    return hour, minute
