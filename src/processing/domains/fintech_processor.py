import pandas as pd
import numpy as np

def process_fintech(df):

    df["event_time"] = pd.to_datetime(df["timestamp"], format="mixed")
    df["event_hour"] = df["event_time"].dt.hour

    # Base features
    df["high_value_txn"] = (df["transaction_amount"] > 500).astype(int)
    df["low_balance"] = (df["account_balance"] < 2000).astype(int)

    # 🔥 Risk score (core signal)
    df["risk_score"] = (
        (df["transaction_amount"] > 4000).astype(int) +
        (df["account_balance"] < 1500).astype(int) +
        (df["event_hour"] > 22).astype(int)
    )

    # 🎯 Target
    df["fraud"] = 0
    df.loc[df["risk_score"] >= 2, "fraud"] = 1

    # ⚠️ Minimal randomness
    mask = np.random.rand(len(df)) < 0.02
    df.loc[mask, "fraud"] = 1
    print("fraud count in batch:",df["fraud"].sum())
    return df