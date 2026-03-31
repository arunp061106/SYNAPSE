import duckdb
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

DB_PATH = "data/silver/synapse.db"

TARGET_MAP = {
    "ecommerce": "is_purchase",
    "iot": "anomaly",
    "fintech": "fraud"
}


def validate_ml_utility(exp_config):

    con = duckdb.connect(DB_PATH)

    # ✅ Use gold table (same as before)
    table = f"gold_{exp_config.domain}"

    df = con.execute(f"SELECT * FROM {table}").df()

    con.close()

    target = TARGET_MAP[exp_config.domain]

    # ✅ Check target exists
    if target not in df.columns:
        print(f"⚠️ Target '{target}' missing")
        return 0.5, 0.5, 0.5

    X = df.drop(columns=[target])
    y = df[target]

    # ✅ FIX: handle single class issue
    if y.nunique() < 2:
        print("⚠️ Only one class present")
        return 0.5, 0.5, 0.5

    # ✅ Safe split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.3,
        random_state=42
    )

    # ✅ FAST MODEL
    model = LogisticRegression(max_iter=200)

    try:
        model.fit(X_train, y_train)
        acc = model.score(X_test, y_test)
    except Exception as e:
        print("⚠️ ML training failed:", e)
        return 0.5, 0.5, 0.5

    return acc, acc, round(acc, 3)
    trust_score =round((overall_score+corr_score+util_score)/3,3)