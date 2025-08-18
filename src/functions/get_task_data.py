import pandas as pd


def get_task_data(task_file):
    task_data = pd.read_csv(task_file, sep=" ")
    task_data.drop(columns=task_data.filter(like="Unnamed").columns, inplace=True)

    return task_data
    