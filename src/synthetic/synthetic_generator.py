import duckdb
import warnings
warnings.filterwarnings("ignore")

from sdv.single_table import CTGANSynthesizer
from sdv.metadata import SingleTableMetadata

DB_PATH = "data/silver/synapse.db"

TABLE_MAP = {
    "ecommerce": "gold_ecommerce",
    "iot": "gold_iot",
    "fintech": "gold_fintech"
}



def generate_synthetic(exp_config, return_model=False):

    # 🔌 Connect DB
    con = duckdb.connect(DB_PATH)

    table = TABLE_MAP[exp_config.domain]

    # 📥 Load real data
    df = con.execute(f"SELECT * FROM {table}").df()
    con.close()

    if df.empty:
        raise ValueError("❌ Gold table is empty. Cannot generate synthetic data.")

    print("\n📊 Real dataset shape:", df.shape)

    # 🧠 Build metadata
    metadata = SingleTableMetadata()
    metadata.detect_from_dataframe(df)

    # ⚙️ Model configuration (balanced for quality + speed)
    print("\n🚀 Starting synthetic training...")

    model = CTGANSynthesizer(
        metadata,
        epochs=20,          # 🔥 increase for better learning
        verbose=True
    )

    model.fit(df)

    print("✅ Finished synthetic training")

    # 🎯 Synthetic size control
    synth_size = int(len(df) * exp_config.synthetic_ratio)

    print(f"\n📦 Generating {synth_size} synthetic rows...")

    synthetic_df = model.sample(synth_size)

    print("✅ Synthetic generation complete")

    # 🔍 Basic sanity check
    print("\n📊 Synthetic dataset shape:", synthetic_df.shape)

    # Optional: return model for reuse (UI optimization later)
    if return_model:
        return synthetic_df, model

    return synthetic_df