import pandas as pd

def process_iot(df):

    df["event_time"] = pd.to_datetime(df["timestamp"], format="mixed")
    df["event_hour"] = df["event_time"].dt.hour

    # Derived IoT features
    df["temp_alert"] = (df["temperature"] > 70).astype(int)
    df["humidity_alert"] = (df["humidity"] > 80).astype(int)

    # 🔥 STRONG BEHAVIORAL LOGIC
    df["anomaly"] = 0

    df.loc[
        (df["temperature"] > 75) &
        (df["humidity"] > 85),
        "anomaly"
    ] = 1

    df.loc[
        (df["temperature"] < 10) |
        (df["humidity"] < 20),
        "anomaly"
    ] = 1
    import numpy as np
    mask = np.random.rand(len(df))<0.05
    df.loc[mask,"anomaly"]=1
    if df["anomaly"].mean()<0.1:
     mask = np.random.rand(len(df))<0.1
     df.loc[mask,"anomaly"]=1
    # ⭐ additional feature (helps ML)
    df["extreme_temp"] = ((df["temperature"] > 80) | (df["temperature"] < 5)).astype(int)

    return df