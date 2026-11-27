from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"

instances = pd.read_csv(RAW_DIR / "instances.csv")
metrics = pd.read_csv(RAW_DIR / "instance_metrics.csv", parse_dates=["timestamp"])

print(instances.shape)
print(metrics.shape)

def calculate_daily_compute_costs(instances: pd.DataFrame, metrics: pd.DataFrame) -> pd.DataFrame:

    df = pd.merge(metrics, instances, on="instance_id", how='left', validate="many_to_one")

    df['date'] = pd.to_datetime(df['timestamp']).dt.date

    res = df.groupby(['instance_type','date']).agg(total_cost=('hourly_cost','sum'),instance_count=('instance_id','nunique'))
    res = res.reset_index(drop=False)

    return res

def calculate_hourly_utilization(instances: pd.DataFrame, metrics: pd.DataFrame) -> pd.DataFrame:

    df = pd.merge(metrics, instances, on="instance_id", how='left', validate="many_to_one")

    df["cpu_observed_capacity"] = df["cpu_count"].where(df["cpu_util"].notna(), 0)
    df["gpu_observed_capacity"] = df["gpu_count"].where(df["gpu_util"].notna(), 0)

    df['util_cpu_capacity'] = df['cpu_count'] * df['cpu_util']
    df['util_gpu_capacity'] = df['gpu_count'] * df['gpu_util']

    res = df.groupby('timestamp', as_index=False).\
        agg(cpu_util_total=("util_cpu_capacity", "sum"),
            gpu_util_total=("util_gpu_capacity", "sum"),
            cpu_observed=("cpu_observed_capacity", "sum"),
            gpu_observed=("gpu_observed_capacity", "sum"),
            cpu_total=("cpu_count", "sum"),
            gpu_total=("gpu_count", "sum")).\
        assign(cpu_util_weighted=lambda d: (d["cpu_util_total"] / d["cpu_observed"]),
               gpu_util_weighted=lambda d: (d["gpu_util_total"] / d["gpu_observed"]),
               cpu_coverage=lambda d: (d["cpu_observed"] / d["cpu_total"]),
               gpu_coverage=lambda d: (d["gpu_observed"] / d["gpu_total"]))

    return res[['timestamp','cpu_util_weighted','gpu_util_weighted','cpu_coverage','gpu_coverage']]


daily_compute_costs = calculate_daily_compute_costs(instances, metrics)
x = calculate_hourly_utilization(instances, metrics)

print(x.head(10))
