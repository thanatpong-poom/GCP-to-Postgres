# GCP-to-Postgres

I've done this project since I was assigned to create a way to transfer files from GCP to on-premise database(Postgres). At the first time, I tended to deploy this function on google cloud composer or airflow on GCP since it is easier to monitor and has a web user interface, but my team says this script will run only once a month. Therefore, I offer this method which is writing a python script and bash script and deploy on Cloud function on GCP to run periodically because it will charge only when the script runs. 

<img width="803" alt="image" src="https://user-images.githubusercontent.com/102346723/213925839-4c95d63e-0caa-4b6a-9857-2d5305a91662.png">

