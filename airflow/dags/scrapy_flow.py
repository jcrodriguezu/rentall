import json
from datetime import timedelta

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator

from pymongo import MongoClient

from providers.scrapy.operator.scrapy import ScrapyOperator
from scrapers.espacio_urbano_spider import EspacioUrbanoPageSpider
from scrapers.espacio_urbano_spider import EspacioUrbanoItemSpider


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
    'airflow-scrapy',
    default_args=default_args,
    description='A simple example of airflow with scrapy'
    # schedule_interval=timedelta(days=1),
)


def get_db_connection():
    client = MongoClient('mongodb://rental_db:27017/rentals')
    db = client['rentals']
    return db['houses_data']


def db_insert(file_name):
    with open(file_name) as jsonf:
        data = json.load(jsonf)
        db = get_db_connection()
        db.insert_many(data)


scrapy_page_op = ScrapyOperator(
    task_id='scrape_pages',
    provide_context=True,
    scraper_cls=EspacioUrbanoPageSpider,
    dag=dag
)

scrapy_item_op = ScrapyOperator(
    task_id='scrape_items',
    provide_context=True,
    scraper_cls=EspacioUrbanoItemSpider,
    scraper_settings={
        'FEED_FORMAT': 'json',
        'FEED_URI': f'/scrapers-data/json/{EspacioUrbanoItemSpider.__name__}.json'
        },
    dag=dag
)

store_items_op = PythonOperator(
    task_id='store_items',
    python_callable=db_insert,
    op_kwargs={'file_name': f'/scrapers-data/json/{EspacioUrbanoItemSpider.__name__}.json'},
    dag=dag
)

scrapy_page_op >> scrapy_item_op >> store_items_op

# pendiente: ver como se puede ejecutar los scraper de scrapy desde airflow
