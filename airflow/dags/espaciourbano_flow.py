from datetime import timedelta

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator

from providers.scrapy.operator.scrapy import ScrapyOperator

from scrapers.settings import SCRAPER_SETTINGS
from scrapers.settings import get_feed_settings
from scrapers.espacio_urbano_spider import EspacioUrbanoPageSpider
from scrapers.espacio_urbano_spider import EspacioUrbanoItemSpider

from utils.database import db_inser_file


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
    'espaciourbano-scrapy',
    default_args=default_args,
    description='Espacio urbano scrapy'
    # schedule_interval=timedelta(days=1),
)

clean_json_dir = BashOperator(
    task_id='clean_json_directory',
    bash_command=f'rm /scrapers-data/json/{EspacioUrbanoItemSpider.__name__}.* 2> /dev/null || echo > /dev/null',
    trigger_rule='all_done',
    dag=dag
)

clean_html_dir = BashOperator(
    task_id='clean_html_directory',
    bash_command=f'rm /scrapers-data/html/{EspacioUrbanoPageSpider.name}*.* 2> /dev/null || echo > /dev/null',
    trigger_rule='all_done',
    dag=dag
)

scrapy_page_op = ScrapyOperator(
    task_id='scrape_pages',
    provide_context=True,
    scraper_cls=EspacioUrbanoPageSpider,
    scraper_settings=SCRAPER_SETTINGS,
    trigger_rule='all_done',
    dag=dag
)

scrapy_item_op = ScrapyOperator(
    task_id='scrape_items',
    provide_context=True,
    scraper_cls=EspacioUrbanoItemSpider,
    scraper_settings=get_feed_settings(EspacioUrbanoItemSpider.__name__),
    dag=dag
)

store_items_op = PythonOperator(
    task_id='store_items',
    python_callable=db_inser_file,
    op_kwargs={'file_name': f'/scrapers-data/json/{EspacioUrbanoItemSpider.__name__}.json'},
    dag=dag
)

clean_html_dir >> clean_json_dir >> scrapy_page_op >> scrapy_item_op >> store_items_op
