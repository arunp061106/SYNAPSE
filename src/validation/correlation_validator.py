import duckdb
import numpy as np
from src.synthetic.synthetic_generator import generate_synthetic

DB_PATH = "data/silver/synapse.db"

TABLE_MAP = {
    "ecommerce": "gold_ecommerce",
    "iot": "gold_iot",
    "fintech": "gold_fintech"
}


def validate_correlation(exp_config):

    con = duckdb.connect(DB_PATH)

    table = TABLE_MAP[exp_config.domain]

    real_df = con.execute(f"SELECT * FROM {table}").df()
    con.close()

    # Generate synthetic dataset
    synth_df = generate_synthetic(exp_config)

    real_num = real_df.select_dtypes(include="number")
    synth_num = synth_df.select_dtypes(include="number")

    # Align columns
    common_cols = list(set(real_num.columns) & set(synth_num.columns))

    real_corr = real_num[common_cols].corr().values
    synth_corr = synth_num[common_cols].corr().values

    # Compute difference
    diff = np.nanmean(np.abs(real_corr - synth_corr))

    corr_score = round(1 - diff, 3)

    return real_corr, synth_corr, diff, corr_score