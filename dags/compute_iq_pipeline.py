
from datetime import timedelta

import pendulum
from airflow.sdk import dag, task


@dag(
    dag_id="compute_iq_pipeline",
    schedule="0 2 * * *",
    start_date=pendulum.datetime(
        2026, 11, 1, tz="America/Los_Angeles"
    ),
    catchup=False,
    tags=["compute_iq"],
)
def compute_iq_pipeline():

    @task(
        retries=2,
        retry_delay=timedelta(minutes=5)
    )
    def ingest_raw_data():
        print("Ingesting raw infrastructure data")

    @task
    def run_dbt():
        print("Running dbt transformations")

    @task
    def validate_data():
        print("Validating data quality")

    @task
    def reconcile_billing():
        print("Reconciling billing records")

    ingest = ingest_raw_data()
    transform = run_dbt()
    validate = validate_data()
    reconcile = reconcile_billing()

    ingest >> transform >> validate >> reconcile


compute_iq_pipeline()
