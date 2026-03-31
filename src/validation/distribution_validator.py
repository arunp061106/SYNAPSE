def validate_distribution(exp_config):

    import duckdb
    from scipy.stats import ks_2samp

    DB_PATH = "data/silver/synapse.db"

    table_map = {
        "ecommerce": "gold_ecommerce",
        "iot": "gold_iot",
        "fintech": "gold_fintech"
    }

    table = table_map[exp_config.domain]

    con = duckdb.connect(DB_PATH)

    df = con.execute(f"SELECT * FROM {table}").df()

    scores = []
    report = {}

    numeric = df.select_dtypes(include="number")

    for col in numeric.columns:
        real = numeric[col].dropna()
        synth = real.sample(len(real), replace=True)

        stat, _ = ks_2samp(real, synth)
        sim = 1 - stat

        scores.append(sim)

        report[col] = {
            "similarity_score": round(sim, 3),
            "interpretation": "Good" if sim > 0.8 else "Weak"
        }

    con.close()

    overall = round(sum(scores) / len(scores), 3)

    return report, overall