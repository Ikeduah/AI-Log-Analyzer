import pandas as pd

def parse_log(file):
    df = pd.read_csv(file, sep=" ", header=None, names=["date", "time", "level", "message"])
    df["timestamp"] = pd.to_datetime(df["date"] + " " + df["time"])
    return df[["timestamp", "level", "message"]]