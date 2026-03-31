import random
import os
import duckdb as db

from src.world.event_generator import UserSimulator
from src.pipeline.event_queue import EventQueue
from src.processing.event_processor import process_events
from src.storage.silver_loader import load_to_silver
from src.storage.gold_mart import build_gold_mart
from src.monitoring.pipeline_metrics import PipelineMonitor
from src.synthetic.synthetic_generator import generate_synthetic
from src.validation.distribution_validator import validate_distribution
from src.validation.correlation_validator import validate_correlation
from src.validation.ml_utility_validator import validate_ml_utility
from src.validation.trust_scorer import compute_trust_score
from src.config.experiment_config import ExperimentConfig

BRONZE_PATH = "data/bronze/events.jsonl"
DB_PATH = "data/silver/synapse.db"


def run_simulation(exp_config):

    users = [UserSimulator(i, exp_config.domain) for i in range(1, 100)]

    monitor = PipelineMonitor()
    TOTAL_EVENTS = exp_config.dataset_size

    print("\n🚀 Running FAST MODE...\n")

    # ---------------- FAST GENERATION ----------------
    all_events = []

    for i in range(TOTAL_EVENTS):

        if i % 1000 == 0:
            print(f"Generated {i} events...")

        user = random.choice(users)
        event = user.generate_event()

        all_events.append(event)

    # ---------------- PROCESS ONCE ----------------
    df = process_events(all_events)

    # ---------------- LOAD ONCE ----------------
    load_to_silver(df)

    monitor.record_batch(len(df))

    # ---------------- GOLD ----------------
    build_gold_mart(exp_config)

    # ---------------- SYNTHETIC ----------------
    synthetic_df = generate_synthetic(exp_config)

    print("\nSynthetic dataset preview:")
    print(synthetic_df.head())

    # ---------------- METRICS ----------------
    metrics = monitor.report()
    print("\nPipeline Metrics:", metrics)

    dist_report, overall_score = validate_distribution(exp_config)

    print("\nDistribution Validation Report:")
    for feature, info in dist_report.items():
        print(f"{feature} → {info['interpretation']} ({info['similarity_score']})")

    print("\nOverall Distribution Score:", overall_score)

    _, _, _, corr_score = validate_correlation(exp_config)
    print("\nCorrelation Score:", corr_score)

    acc1, acc2, util_score = validate_ml_utility(exp_config)

    print("\nML Utility:")
    print("Real → Synthetic:", acc1)
    print("Synthetic → Real:", acc2)
    print("Utility Score:", util_score)

    trust_score, trust_level = compute_trust_score(
        overall_score, corr_score, util_score
    )

    print("\nTrust Score:", trust_score)
    print("Trust Level:", trust_level)

    return {
        "distribution": overall_score,
        "correlation": corr_score,
        "ml_utility": util_score,
        "trust_score": trust_score,
        "total_rows":len(synthetic_df),
        "synthetic_head": synthetic_df.head(),
        "synthetic_full": synthetic_df
    }

    # ---------------- GOLD ----------------
    build_gold_mart(exp_config)

    # ---------------- SYNTHETIC ----------------
    synthetic_df = generate_synthetic(exp_config)

    print("\nSynthetic dataset preview:")
    print(synthetic_df.head())

    # ---------------- METRICS ----------------
    metrics = monitor.report()
    print("\nPipeline Metrics:", metrics)

    dist_report, overall_score = validate_distribution(exp_config)

    print("\nDistribution Validation Report:")
    for feature, info in dist_report.items():
        print(f"{feature} → {info['interpretation']} ({info['similarity_score']})")

    print("\nOverall Distribution Score:", overall_score)

    _, _, _, corr_score = validate_correlation(exp_config)
    print("\nCorrelation Score:", corr_score)

    acc1, acc2, util_score = validate_ml_utility(exp_config)

    print("\nML Utility:")
    print("Real → Synthetic:", acc1)
    print("Synthetic → Real:", acc2)
    print("Utility Score:", util_score)

    trust_score, trust_level = compute_trust_score(
        overall_score, corr_score, util_score
    )

    print("\nTrust Score:", trust_score)
    print("Trust Level:", trust_level)
    return {
    "distribution": overall_score,
    "correlation": corr_score,
    "ml_utility": util_score,
    "trust_score": trust_score,
    "synthetic_head": synthetic_df.head(),
    "synthetic_full": synthetic_df
}

# ---------------- ENTRY ----------------

if __name__ == "__main__":

    try:
        domain = input("Domain (ecommerce / iot / fintech): ").strip().lower()
        size = int(input("Dataset size: "))
        ratio = float(input("Synthetic ratio: "))

    except ValueError:
        print(" Invalid input")
        exit()

    exp = ExperimentConfig(
        dataset_size=size,
        synthetic_ratio=ratio,
        domain=domain
    )

    run_simulation(exp)
    