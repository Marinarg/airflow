"""
## DAG Documentation
This DAG is responsible for generating the Kmeans model that will be used in the website's recommendation system
"""
import nltk
import pickle
import mysql.connector

from datetime import datetime
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

from airflow import DAG
from airflow.operators.python import PythonOperator

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

MODEL_PATH = '/home/admin/kmeans_model.sav'

# FUNCTIONS
def generate_recommendation_model(**kwargs):
    # MySQL connect
    connection = mysql.connector.connect(host='localhost',
                                         database='eletronics',
                                         user='root',
                                         password='pankeka123')

    # Get stop words
    nltk.download('stopwords')
    nltk_stop_words = nltk.corpus.stopwords.words('portuguese')

    my_stop_words = [
        "características", "linear", "strong", "ref", "span", "div", "td", "tr", "table", "projetos", "chave", "possui",
        "tolerância", "tensão", "w", "awg", "utilizado", "kit", "ser", "dr"]

    stop_words = nltk_stop_words + my_stop_words

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
generate_files_task = PythonOperator(
        task_id=f"generate_model",
        python_callable=generate_recommendation_model,
        dag=dag,
    )

generate_files_task
