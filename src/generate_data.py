import random
import numpy as np
import pandas as pd
from pathlib import Path

# Project root (assuming this file is in src/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

INSTANCE_TYPES = {
    "cpu-small": {
        "cpu_count": 4,
        "gpu_count": 0,
        "hourly_cost": 0.20,
    },
    "cpu-large": {
        "cpu_count": 16,
        "gpu_count": 0,
        "hourly_cost": 0.80,
    },
    "gpu-small": {
        "cpu_count": 8,
        "gpu_count": 1,
        "hourly_cost": 2.50,
    },
    "gpu-large": {
        "cpu_count": 32,
        "gpu_count": 4,
        "hourly_cost": 10.00,
    },
}

def generate_instances(n_instances: int, seed: int = 42) -> pd.DataFrame:

    rng = random.Random(seed)

    instances = []

    for i in range(n_instances):

        # 1. Generate instance_id: i-001, i-002...
        instance_id = f"i-{i + 1:03d}"

        # 2. Randomly select instance_type
        instance_type = rng.choice(list(INSTANCE_TYPES))

        # 3. Retrieve configuration from INSTANCE_TYPES
        config = INSTANCE_TYPES[instance_type]

        # 4. Append a dictionary to instances
        instances.append({'instance_id':instance_id, 'instance_type':instance_type, **config})

    return pd.DataFrame(instances)

def generate_instance_metrics(instances: pd.DataFrame, n_days: int = 30, seed: int = 42) -> pd.DataFrame:

    rng = np.random.default_rng(seed)

    size = n_days * 24

    timestamps = pd.date_range(start="2026-10-01", periods=size, freq="h", tz="UTC")
    hours = timestamps.hour.to_numpy()
    daily_pattern = np.sin(2 * np.pi * (hours - 12) / 24)

    profile_config = {'underutilized':[0.15, 0.03, 0.05],'normal':[0.50, 0.08, 0.25],'heavy':[0.85, 0.05, 0.10]}

    metrics = []

    for row in instances.itertuples(index=False):
        instance_id = row.instance_id
        profile = rng.choice(["underutilized", "normal", "heavy"], p=[0.25, 0.50, 0.25])
        mean, std, amplitude = profile_config[profile]

        cpu_util = (mean + amplitude * daily_pattern + rng.normal(0, std, size)).clip(0, 1)
        gpu_util = (mean + amplitude * daily_pattern + rng.normal(0, std, size)).clip(0, 1) if row.gpu_count > 0 else np.full(size, np.nan)

        for index, timestamp in enumerate(timestamps):
            metrics.append({'instance_id':instance_id, 'timestamp':timestamp, 'cpu_util':cpu_util[index], 'gpu_util':gpu_util[index]})

    return pd.DataFrame(metrics)

instances = generate_instances(100)
metrics = generate_instance_metrics(instances)

assert len(instances) == 100
assert instances["instance_id"].is_unique
assert instances.equals(generate_instances(100))

assert len(metrics) == 100 * 30 * 24
assert not metrics.duplicated(["instance_id", "timestamp"]).any()
assert metrics["cpu_util"].between(0, 1).all()
assert metrics["gpu_util"].dropna().between(0, 1).all()

instances.to_csv(RAW_DIR / "instances.csv", index=False)
metrics.to_csv(RAW_DIR / "instance_metrics.csv", index=False)