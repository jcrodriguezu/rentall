FROM puckel/docker-airflow:1.10.6

RUN pip install --user psycopg2-binary

COPY ./requirements.txt .
RUN pip install --user -r requirements.txt

ENV AIRFLOW_HOME=/usr/local/airflow
COPY ./config/airflow.cfg /usr/local/airflow/airflow.cfg