"""
## DAG Documentation
This DAG is responsible for generating the Kmeans model that will be used in the website's recommendation system
"""
import json
import nltk
import pickle
import mysql.connector

from datetime import datetime
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

from airflow import DAG
from airflow.models import TaskInstance
from airflow.operators.python import PythonOperator

# DAG DEFINITIONS
default_args = {
    "email": "marinarg09@gmail.com",
    "email_on_failure": True,
}
dag = DAG(
        dag_id="recommendations_model_generator",
        schedule_interval="0 12 * * *",
        start_date=datetime(2021, 1, 1),
        catchup=False,
        default_args=default_args
)

# GLOBAL VARIABLES
STOP_WORDS_PATH = '/home/admin/stop_words.json'
MODEL_PATH = '/home/admin/kmeans_model.sav'

# FUNCTIONS
def generate_stop_words():
    # Get stop words
    nltk.download('stopwords')
    nltk_stop_words = nltk.corpus.stopwords.words('portuguese')

    my_stop_words = [
        "características", "linear", "strong", "ref", "span", "div", "td", "tr", "table", "projetos", "chave", "possui",
        "tolerância", "tensão", "w", "awg", "utilizado", "kit", "ser", "dr"]

    stop_words = nltk_stop_words + my_stop_words

    # Save it in a json file to use in website API
    with open(STOP_WORDS_PATH, 'w') as f:
        f.write(json.dumps({"stop_words": stop_words}))

    return stop_words


def generate_recommendation_model(**kwargs):
    # Get stop words
    ti: TaskInstance = kwargs["ti"]
    stop_words = ti.xcom_pull(task_ids="generate_stop_words")

    # MySQL connect
    connection = mysql.connector.connect(host='localhost',
                                         database='eletronics',
                                         user='root',
                                         password='pankeka123')


    # Get product descriptions and vectorize it (considering stop words)
    sql_get_descriptions_query = (
        """
        SELECT DISTINCT product_description 
        FROM crawlers_results;
        """
    )

    cursor = connection.cursor()
    cursor.execute(sql_get_descriptions_query)
    records = cursor.fetchall()

    product_descriptions = [item[0] for item in records]

    tfid_vectorizer = TfidfVectorizer(stop_words=stop_words)
    vectorized_descriptions = tfid_vectorizer.fit_transform(product_descriptions)

    # Use Kmeans to get a recommendation model
    model = KMeans(n_clusters=20, init='k-means++', max_iter=100, n_init=1)
    model.fit(vectorized_descriptions)

    # Save model
    pickle.dump(model, open(MODEL_PATH, 'wb'))

    return None


# TASKS
generate_stop_words_file = PythonOperator(
    task_id=f"generate_stop_words",
    python_callable=generate_stop_words,
    dag=dag,
)

generate_files_task = PythonOperator(
    task_id=f"generate_model",
    python_callable=generate_recommendation_model,
    dag=dag,
)

generate_stop_words_file >> generate_files_task
