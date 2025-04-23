from time import localtime, strftime


def get_current_time():
    return strftime("%Y-%m-%d %H:%M:%S", localtime())


def get_hour_minute():
    return int(strftime("%H", localtime())), int(strftime("%M", localtime()))


def get_next_quarter(hour, minute):
    remaining = minute % 15
    minute += 15 - remaining
    minute %= 60

    if remaining != 0 and minute % 60 == 0:
        return (hour + 1) % 24, minute
    return hour, minute


def get_index_quarter(hour, minute):
    return 4 * hour + int(minute // 15)


def get_quarter_time(index):
    hour = (index // 4) % 24
    minute = 15 * (index % 4)
    return hour, minute
