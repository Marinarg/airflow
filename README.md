# Airflow

Dedicated repository for storing Airflow DAGs. So far there are 8 DAGs:

- **daily_crawler_baudaeletronica**
- **daily_crawler_baudaeletronica_shipping**
- **daily_crawler_digikey**
- **daily_crawler_filipeflop**
- **daily_crawler_filipeflop_shipping**
- **daily_crawler_soldafria**
- **daily_crawler_tiggercomp**
- **daily_generate_kmeans_model**

## DAGs

All DAGs (with the exception of the **daily_generate_kmeans_model**) have the following 5 tasks:

- **dummy_task**: has a DummyOperator just to prepare for the next task;
- **trigger_crawler**: has a BashOperator to trigger the spider via Scrapy command and to export results to a CSV file;
- **move_result_files**: has a BashOperator to move the file generated on the last task to MySQL default files folder located on `/var/lib/mysql-files/`;
- **update_mysql_table**: has a MySqlOperator to ingest data from file moved on the last task to MySQL default files folder;
- **delete_csv_file**: has a BashOperator to delete file generated on **trigger_crawler** task.

The **daily_generate_kmeans_model** tasks will be presented in its section.


### daily_crawler_baudaeletronica
This DAG is mainly responsible for running [baudaeletronica spider](https://github.com/Marinarg/my_crawlers/blob/main/websites_crawlers/spiders/baudaeletronica.py) located at [My Crawlers](https://github.com/Marinarg/my_crawlers) repository. [Here](dags/
daily_crawler_baudaeletronica.py) is the link to this DAG.


### daily_crawler_baudaeletronica_shipping
This DAG is mainly responsible for running [baudaeletronica spider](https://github.com/Marinarg/my_crawlers/blob/main/websites_crawlers/spiders/baudaeletronica_shipping.py) located at [My Crawlers](https://github.com/Marinarg/my_crawlers) repository. [Here](dags/
daily_crawler_baudaeletronica_shipping.py) is the link to this DAG.


### daily_crawler_digikey
This DAG is mainly responsible for running [baudaeletronica spider](https://github.com/Marinarg/my_crawlers/blob/main/websites_crawlers/spiders/digikey.py) located at [My Crawlers](https://github.com/Marinarg/my_crawlers) repository. [Here](dags/
daily_crawler_digikey.py) is the link to this DAG.


### daily_crawler_filipeflop
This DAG is mainly responsible for running [baudaeletronica spider](https://github.com/Marinarg/my_crawlers/blob/main/websites_crawlers/spiders/filipeflop.py) located at [My Crawlers](https://github.com/Marinarg/my_crawlers) repository. [Here](dags/
daily_crawler_filipeflop.py) is the link to this DAG.


### daily_crawler_filipeflop_shipping
This DAG is mainly responsible for running [baudaeletronica spider](https://github.com/Marinarg/my_crawlers/blob/main/websites_crawlers/spiders/filipeflop_shipping.py) located at [My Crawlers](https://github.com/Marinarg/my_crawlers) repository. [Here](dags/
daily_crawler_filipeflop_shipping.py) is the link to this DAG.

### daily_crawler_soldafria
This DAG is mainly responsible for running [baudaeletronica spider](https://github.com/Marinarg/my_crawlers/blob/main/websites_crawlers/spiders/soldafria.py) located at [My Crawlers](https://github.com/Marinarg/my_crawlers) repository. [Here](dags/
daily_crawler_soldafria.py) is the link to this DAG.

### daily_crawler_tiggercomp
This DAG is mainly responsible for running [baudaeletronica spider](https://github.com/Marinarg/my_crawlers/blob/main/websites_crawlers/spiders/tiggercomp.py) located at [My Crawlers](https://github.com/Marinarg/my_crawlers) repository. [Here](dags/
daily_crawler_tiggercomp.py) is the link to this DAG.

### daily_generate_kmeans_model

This DAG is responsible for generating the Kmeans model that will be used in the [ebusca website](http://ebusca.link/) recommendation system. This model is generated based on the product descriptions found by the crawlers triggered in the DAGs described above. 

This DAG has 2 tasks:

- **generate_stop_words**: has a PythonOperator to generate the stop words file that will be used by Kmeans model. The file is formed by stop words loaded through the Python nltk library together with words added manually after some remarks in the result of the product descriptions found by crawlers.
- **generate_model**: has a PythonOperator to train and save the final Kmeans model on a file.



