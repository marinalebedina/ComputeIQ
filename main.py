from src.load_data import load_idempotently
from sqlalchemy import create_engine
from pathlib import Path
import pandas as pd
import os

def main():

    PROJECT_ROOT = Path(__file__).resolve().parent
    RAW_DIR = PROJECT_ROOT / "data" / "raw"

    DATABASE_URL = os.getenv("COMPUTEIQ_DATABASE_URL",
                             "postgresql+psycopg://computeiq:computeiq_dev@127.0.0.1:5433/computeiq")
    engine = create_engine(DATABASE_URL)

    instances = pd.read_csv(RAW_DIR / "instances.csv")
    metrics = pd.read_csv(RAW_DIR / "instance_metrics.csv", parse_dates=["timestamp"])

    load_idempotently(engine, instances, metrics)

    print("Data loaded successfully!")

if __name__ == "__main__":
    main()