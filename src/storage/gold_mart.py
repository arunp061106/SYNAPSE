import duckdb

DB_PATH = "data/silver/synapse.db"

def build_gold_mart(exp_config):

    con = duckdb.connect(DB_PATH)

    domain = exp_config.domain

    # ---------------- ECOMMERCE ----------------
    if domain == "ecommerce":

        con.execute("""
            CREATE OR REPLACE TABLE gold_ecommerce AS
            SELECT
                entity_id as user_id,
                event_hour,
                transaction_amount,
                is_purchase
            FROM events
            WHERE domain = 'ecommerce'
        """)

    # ---------------- IOT ----------------
    elif domain == "iot":

        con.execute("""
            CREATE OR REPLACE TABLE gold_iot AS
            SELECT
                entity_id as device_id,
                event_hour,
                temperature,
                humidity,
                anomaly
            FROM events
            WHERE domain = 'iot'
        """)

    # ---------------- FINTECH ----------------
    elif domain == "fintech":

        con.execute("""
            CREATE OR REPLACE TABLE gold_fintech AS
            SELECT
                entity_id as user_id,
                event_hour,
                transaction_amount,
                account_balance,
                fraud
            FROM events
            WHERE domain = 'fintech'
        """)

    # ✅ DEBUG (optional but useful)
    try:
        if domain == "fintech":
            print("\nFraud distribution:")
            print(con.execute(
                "SELECT fraud, COUNT(*) FROM gold_fintech GROUP BY fraud"
            ).fetchall())
    except:
        pass

    con.close()