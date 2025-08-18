

def get_sec_total(time_str):
    unit_list = time_str.split(':')
    hours, minutes, seconds, milliseconds = map(int, unit_list)
    sec_total = hours * 3600 + minutes * 60 + seconds + milliseconds / 1000

    return sec_total
