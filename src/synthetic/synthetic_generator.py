import duckdb
import pandas as pd
import numpy as np

DB_PATH = "data/silver/synapse.db"

# ---------------- OPTIONAL SDV ----------------
try:
    from sdv.single_table import CTGANSynthesizer
    SDV_AVAILABLE = True
except:
    SDV_AVAILABLE = False


TABLE_MAP = {
    "ecommerce": "gold_ecommerce",
    "iot": "gold_iot",
    "fintech": "gold_fintech"
}


def generate_synthetic(exp_config):

    con = duckdb.connect(DB_PATH)

    table = TABLE_MAP[exp_config.domain]

    df = con.execute(f"SELECT * FROM {table}").df()

    con.close()

    if df is None or df.empty:
        print("⚠️ No data found for synthetic generation")
        return pd.DataFrame()

    # ---------------- SIZE ----------------
    num_rows = int(len(df) * exp_config.synthetic_ratio)

    # ---------------- SDV PATH ----------------
    if SDV_AVAILABLE:
        try:
            print("🚀 Using CTGAN (SDV)")

            model = CTGANSynthesizer()
            model.fit(df)

            synthetic = model.sample(num_rows)

        except Exception as e:
            print("⚠️ SDV failed, switching to fallback:", e)
            synthetic = fallback_generation(df, num_rows)

    else:
        print("⚠️ SDV not available, using fallback")
        synthetic = fallback_generation(df, num_rows)

    return synthetic


# ---------------- FALLBACK GENERATOR ----------------
def fallback_generation(df, num_rows):

    synthetic = df.sample(n=num_rows, replace=True).reset_index(drop=True)

    # 🔥 Add small noise to numeric columns
    numeric_cols = synthetic.select_dtypes(include="number").columns

    for col in numeric_cols:
        noise = np.random.normal(0, 0.01, size=len(synthetic))
        synthetic[col] = synthetic[col] * (1 + noise)

    # 🔥 Ensure target columns still valid (0/1)
    for target in ["fraud", "is_purchase", "anomaly"]:
        if target in synthetic.columns:
            synthetic[target] = synthetic[target].round().clip(0, 1)

    return synthetic
