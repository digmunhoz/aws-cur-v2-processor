# AWS Cur V2 Processor

This project is a worker designed to process Parquet files and store the data in Elasticsearch, following the "ports and adapters" architecture.

## Prerequisites
Ensure you have the following software installed:

- Docker
- Docker Compose

## Setup and Usage
The system uses a Makefile for easy management. Below are the commands you can use:

### Build the Project
Before running the project, you need to build the Docker containers:

```sh
make build
```

### Start the Project
After building, start the project with:

```sh
make start
```

### Run processor
To process all parquet files:

```sh
make cur
```

### Check Container Status
To check the status of the running containers:

```sh
make status
```

### View Logs
To view the logs of the running containers:

```sh
make logs
```

### Stop the Project
To stop all running containers:

```sh
make stop
```

### Processing Parquet Files
Place your .parquet files in the parquet_files directory. After processing, the files will be renamed with the .processed extension.

## Configuration Variables

| Variable Name          | Type    | Default Value | Meaning                                        |
|------------------------|---------|---------------|------------------------------------------------|
| `ELASTICSEARCH_HOST`   | String  | `localhost`   | The host address of the Elasticsearch server   |
| `ELASTICSEARCH_PORT`   | Integer | `9200`        | The port number of the Elasticsearch server    |
| `FILE_THREADS`         | Integer | 2             | How many parquet files will be processed at same time |
| `WORKER_THREADS`       | Integer | 2             | How many workers will be used on elasticsearch bulk insert |
| `STORAGE_TYPE`         | String  | `LOCAL`       | Data source to find parquet files. `LOCAL` or `S3` |
| `AWS_ACCESS_KEY_ID`    | String  |               | AWS Access Key to connect on S3 when using `STORAGE_TYPE` as `S3` |
| `AWS_SECRET_ACCESS_KEY`| String  |               | AWS Access Key ID to connect on S3 when using `STORAGE_TYPE` as `S3` |
| `AWS_REGION`           | String  | `us-east-1`   | AWS region where S3 Bucket was created         |
| `AWS_BUCKET_NAME`      | String  |               | AWS S3 Bucket where parquet files are created  |

## Accessing Grafana
After processing the files, you can access Grafana at:

http://localhost:3000

Use the following credentials:

- Username: admin
- Password: password

Follow these instructions to set up, run, and manage the AWS Cur V2 Processor. Ensure your environment meets the prerequisites and that you follow the steps in the correct order.