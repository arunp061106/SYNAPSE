import pandas as pd

from src.processing.domains.ecommerce_processor import process_ecommerce
from src.processing.domains.iot_processor import process_iot
from src.processing.domains.fintech_processor import process_fintech


def process_events(batch):

    df = pd.DataFrame(batch)

    if "domain" not in df.columns:
        raise ValueError("Event missing domain field")

    processed_frames = []

    for domain, sub_df in df.groupby("domain"):

        if domain == "ecommerce":
            processed = process_ecommerce(sub_df.copy())

        elif domain == "iot":
            processed = process_iot(sub_df.copy())

        elif domain == "fintech":
            processed = process_fintech(sub_df.copy())

        else:
            continue

        processed_frames.append(processed)

    final_df = pd.concat(processed_frames, ignore_index=True)

    return final_df

    df["high_value"]= (df["transaction_amount"]>5000).astype(int)