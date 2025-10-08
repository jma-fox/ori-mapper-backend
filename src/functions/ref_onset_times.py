from datetime import timedelta


def ref_onset_times(task_data, start_time):
    onset_times = []
    for time in task_data['GaborOnsetTm']:
        h, m, s, ms = time.split(':')
        delta = timedelta(hours=int(h), minutes=int(m), seconds=float(s), milliseconds=int(ms))
        onset = delta.total_seconds() - start_time
        onset_times.append(onset)

    task_data["GaborOnsetTm"] = onset_times

    return task_data
