import subprocess

import config as cfg
import util.file as file
import util.date_time as date_time

import api.miele_data as miele
import api.tibber_data as tibber

LOG_FILE = "run.log"


def calculate_prices(price_array, profile_data, max_waiting_quarters, price_offset, step=4):
    if max_waiting_quarters is None:
        max_waiting_quarters = 1
    if price_offset is None:
        price_offset = 0

    max_waiting_quarters = max(max_waiting_quarters, 1)
    price_offset = max(price_offset, 0.01)

    extended_price_array = convert_price_array(price_array, step)

    curr_hour, curr_minute = date_time.get_hour_minute()
    next_h, next_m = date_time.get_next_quarter(curr_hour, curr_minute)

    q_index = date_time.get_index_quarter(next_h, next_m)

    solutions = []
    for t in range(max_waiting_quarters):
        solutions.append(calculate_price(q_index + t, extended_price_array, profile_data))

    min_price = min(solutions)
    min_index = solutions.index(min_price)

    log_prices(solutions, q_index, min_index)

    if solutions[0] - price_offset < min_price:
        min_index = 0
        return True
    return False


def convert_price_array(price_array, step):
    extended_price_array = []
    for price in price_array:
        for _ in range(step):
            extended_price_array.append(price)
    return extended_price_array


def calculate_price(time_offset, price_array, profile_data):
    energy_prices = []

    for t in range(len(profile_data)):
        curr_profile = profile_data[t] * 0.25
        time_index = time_offset + t

        curr_price = price_array[len(price_array) - 1] * curr_profile

        if time_index < len(price_array):
            curr_price = price_array[time_index] * curr_profile

        energy_prices.append(curr_price / 1000)
    return sum(energy_prices)


def log_prices(solutions, q_index, min_index):
    file.msg(cfg.LOG_DIR, LOG_FILE, "\n[~]", " - Calculated Prices")
    for i, sol in enumerate(solutions):
        hour, minute = date_time.get_quarter_time(q_index + i)
        file.update_file(cfg.LOG_DIR, "run.log", f"  {i:02} - {hour:02}:{minute:02} -> {sol:.4f}\n")
    start_hour, start_minute = date_time.get_quarter_time(q_index + min_index)
    file.update_file(cfg.LOG_DIR, "run.log", f"[~] Best Index: {min_index} -> {start_hour:02}:{start_minute:02}\n")


def get_key_value(data, key):
    if key not in data.keys():
        return None
    return data[key]


def main():
    cfg.setup()

    tibber_price = file.get_json_data(cfg.SAVE_DATA_DIR, cfg.TIBBER_DATA_FILE)
    price_array = tibber.get_price_array(tibber_price)

    miele_device_data = file.get_json_data(cfg.SAVE_DATA_DIR, cfg.MIELE_DATA_FILE)
    status_devices = miele.get_status(miele_device_data)

    start_times = miele.get_start_times(miele_device_data)
    program_ids = miele.get_program_ids(miele_device_data)
    ids = miele.get_ids(miele_device_data)

    for i in range(len(status_devices)):
        if miele.device_is_Off(status_devices[i]):
            file.msg(cfg.LOG_DIR, LOG_FILE, "[~]", f"DEVICE: {ids[i]} IS OFF")
            continue

        if miele.device_is_Running(status_devices[i]):
            file.msg(cfg.LOG_DIR, LOG_FILE, "[~]", f"DEVICE: {ids[i]} IS RUNNING")
            continue

        profile_data = file.get_json_data(cfg.SAVE_DATA_DIR, f"{ids[i]}.json")

        if profile_data is None:
            continue

        program_id = program_ids[i]
        program_data = get_key_value(profile_data, str(program_id))
        if program_data is None:
            file.msg(cfg.LOG_DIR, LOG_FILE, "[~]", f"DEVICE: {ids[i]} - NO PROFILE: {program_id}")
            continue

        quarters_left = date_time.get_index_quarter(start_times[i][0], start_times[i][1])
        price_offset = get_key_value(profile_data, "priceOffset")

        start_now = calculate_prices(price_array, program_data, quarters_left, price_offset)

        if start_now:
            file.msg(cfg.LOG_DIR, LOG_FILE, "[~]", f"DEVICE: {ids[i]} START NOW")
            subprocess.run(["python", "main.py", "miele", "start_device", f"{ids[i]}"])
            continue

        file.msg(cfg.LOG_DIR, LOG_FILE, "[~]", f"DEVICE: {ids[i]} START LATER")


if __name__ == "__main__":
    main()
