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


## Installation Instructions

This project currently uses:
- Python 3.6.8
- Airflow 2.1.0

1. Install Miniconda:
- `wget -q https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh`
- `chmod +x Miniconda3-latest-Linux-x86_64.sh`
- `./Miniconda3-latest-Linux-x86_64.sh`
- `export PATH="/home/<YOUR-USER>/miniconda3/bin:$PATH" source ~/.bashrc`

2. Create a Python environment, activate and install requirements:
- `conda create -n airflow python=3.6`
- `conda activate airflow`
- `pip install -r requirements.txt`

## Airflow configuration

### 1. Environment variables
There is one environment variable needed to be configured before using this instance of Airflow that is `AIRFLOW_HOME`. It must contain the full path of the root directory of this repository. To see that, open a terminal and run `pwd` on this repository's root directory. Then, run `export AIRFLOW_HOME=/path/to/repo` replacing the path by what is the correct value for you. To make this variable permanet, you can also add it to your `~/.bashrc` file.

### 2. Local MySQL DB
For Airflow to save the required metadata to run, it needs to store into a database. So you need to download MySQL client and follow [Airflow tutorial](https://airflow.apache.org/docs/apache-airflow/stable/howto/set-up-database.html#setting-up-a-mysql-database).

### 3. Configure `airflow.cfg` file
After configuring the environment variables and the local DB, you can finally add your local configurations to your local Airflow instance. For that, you will have to replace some variables as MySQL DB user and password.

### 4. Initialize the local DB
With all previous steps done, open a terminal, navigate to the repository's root directory and run the command: `airflow db init`.

## Running a DAG / Task

There are 2 ways to test a DAG/task in Airflow while developing.

### 1. `airflow tasks test` command
To run a specific task, use the command:

`airflow tasks test [dag_id] [task_id] [execution_date]`

in which:
- `[dag_id]`: the DAG's name;
- `[task_id]`: the task's name;
- `[execution_date]`: a date in `YYYY-MM-DD` format that is greater than the DAG's `start_date` parameted + 1 schedule interval.

### 2. Scheduler + Webserver
Open 2 terminal sessions, enable the Airflow Conda environment in both of them and run one command in each terminal:

- `airflow webserver`
- `airflow scheduler`

Then, open the browser in the URL http://localhost:8080/, go to the DAG you want to run, unpause it and check the execution and logs.
