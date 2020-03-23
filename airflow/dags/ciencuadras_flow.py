import os
import json
from datetime import timedelta

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator

from providers.scrapy.operator.scrapy import ScrapyOperator

from scrapers.settings import SCRAPER_SETTINGS
from scrapers.cien_cuadras_spider import CienCuadrasItemSpider

from utils.database import db_insert_json


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(2),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'ciencuadras-scrapy',
    default_args=default_args,
    description='Cien cuadras scrapy'
    # schedule_interval=timedelta(days=1),
)


def process_files(name=CienCuadrasItemSpider.name, path='/scrapers-data/json/'):
    file_list = [f.path for f in os.scandir(path=path)
                 if f.is_file() and name in f.name]
    for f in file_list:
        print(f'*********************************processing {f}')
        with open(f) as json_file:
            data = json.load(json_file)
            db_insert_json(data)


scrapy_items_op = ScrapyOperator(
    task_id='scrape-items',
    provide_context=True,
    scraper_cls=CienCuadrasItemSpider,
    scraper_settings=SCRAPER_SETTINGS,
    dag=dag
)

store_items_op = PythonOperator(
    task_id='store_items',
    python_callable=process_files,
    dag=dag
)

scrapy_items_op >> store_items_op


# TODO: crear un spider que procese cada item, filtre los campos y guarde un solo archivo,
# este archivo es el que se guarda en la db