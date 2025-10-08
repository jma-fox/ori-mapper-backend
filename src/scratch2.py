import pandas as pd

file = "/Users/johnamodeo/Desktop/dingo_20250813_AttendGrat_1541.dat"
data = pd.read_csv(file, delimiter=" ", engine="python")
valid_outcomes = ['Correct', 'Miss', 'False', 'Early', 'EarlyFalse']
data.drop(columns=data.filter(like='Unnamed').columns, inplace=True)
data = data[data['Outcome'].isin(valid_outcomes)]

data.to_csv('task_data.csv', index=False)