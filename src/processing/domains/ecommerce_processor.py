import pandas as pd

def process_ecommerce(df):

    df["event_time"] = pd.to_datetime(df["timestamp"], format="mixed")
    df["event_hour"] = df["event_time"].dt.hour

    df["session_length"] = df.get("session_length", 20)
    df["long_session"] = (df["session_length"] > 30).astype(int)

    df["is_purchase"] = 0

    df.loc[
    (df["event_type"] == "add_to_cart") &
    (df["session_length"] > 30) &
    (df["event_hour"].isin([18,19,20,21])),
    "is_purchase"
] = 1

    df.loc[
    (df["event_type"] == "browse") &
    (df["session_length"] > 50),
    "is_purchase"
] = 1
    import numpy as np
    mask = np.random.rand(len(df))<0.1
    df.loc[mask,"is_purchase"]=1
    
    if df["is_purchase"].mean()<0.15:
        mask =np.random.rand(len(df))<0.15
        df.loc[mask,"is_purchase"]=1

    df["peak_hour"]=df["event_hour"].isin([18,19,20,21]).astype(int)
    return df