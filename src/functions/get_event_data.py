import pandas as pd


event_dict = {
    1111.0: 'trial_start',
    1000.0: 'task_on',
    1200.0: 'fix_spot_loaded',
    1202.0: 'fix_spot_on',
    1210.0: 'gaze_in_fix_window',
    1220.0: 'fixating',
    2500.0: 'stim_loaded',
    2502.0: 'rings_on',
    8000.0: 'reward',
    2504.0: 'gabors_presented',
    2501.0: 'stim_off',
    2507.0: 'gabor_change',
    1001.0: 'task_off',
    2503.0: 'rings_removed',
    1201.0: 'fix_spot_off',
    1203.0: 'fix_spot_removed',
    # Address stimulus and trail properties later
    1112.0: 'trial_end'
}

def get_event_data(tdt_data, start_time, stop_time):
    events = tdt_data["epocs"]["eve_"]["data"][0]
    times = tdt_data["epocs"]["eve_"]["onset"][0]
    event_data = pd.DataFrame({"events": events, "times": times})
    event_data = event_data[(event_data['times'] > start_time) & (event_data['times'] < stop_time)]

    event_data = event_data[event_data["events"].isin(list(event_dict.keys()))]
    event_data['events'] = [event_dict[e] for e in event_data['events']]

    trial_count = 0
    trial_list = []
    for event in event_data['events']:
        if event == 'trial_start':
            trial_count += 1
        trial_list.append(trial_count)
        
    event_data['trials'] = trial_list

    return event_data
