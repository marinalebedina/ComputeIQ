FROM apache/airflow:3.1.3

COPY --chown=airflow:root requirements.txt /opt/airflow/requirements.txt

RUN pip install --no-cache-dir -r /opt/airflow/requirements.txt

COPY --chown=airflow:root src/ /opt/airflow/src/
COPY --chown=airflow:root main.py /opt/airflow/main.py

ENV PYTHONPATH=/opt/airflow