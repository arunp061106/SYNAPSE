import duckdb

DB_PATH = "data/silver/synapse.db"

def load_to_silver(df):

    con = duckdb.connect(DB_PATH)

    con.register("df_temp", df)

    # ✅ SINGLE TABLE WRITE (NO LOOP)
    con.execute("""
        CREATE OR REPLACE TABLE events AS
        SELECT * FROM df_temp
    """)

    con.close()