import pandas as pd


def get_onset_data(task_data, event_data, event_name='stim_loaded'):
    correct_trials = task_data[task_data['Outcome'] == 'Correct'].copy()
    correct_trials['Tcnt'] = [int(trial) for trial in correct_trials['Tcnt']]
    onset_events = event_data[event_data['events'] == event_name].copy()
    onset_events['trials'] = [int(trial) for trial in onset_events['trials']]

    trials = []
    for i, trial_row in correct_trials.iterrows():
        trial_number = correct_trials.loc[i, 'Tcnt']
        if trial_number in list(onset_events['trials']):
            onset_event = onset_events[onset_events['trials'] == trial_number].iloc[0]
            trial_row['OnsetTm'] = onset_event['times']
            trials.append(trial_row)

    onset_data = pd.DataFrame(trials)

    return onset_data
