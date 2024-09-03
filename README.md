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
| `OUTPUT_ADAPTER`       | String  | `opensearch`  | Where data will be saved after being processed. `opensearch` or `elasticsearch` |
| `OUTPUT_ADAPTER_HOST`  | String  | `localhost`   | The host address of the Elasticsearch server   |
| `OUTPUT_ADAPTER_PORT`  | Integer | `9200`        | The port number of the Elasticsearch server    |
| `FILE_THREADS`         | Integer | 2             | How many parquet files will be processed at same time |
| `WORKER_THREADS`       | Integer | 2             | How many workers will be used on elasticsearch bulk insert |
| `STORAGE_TYPE`         | String  | `LOCAL`       | Data source to find parquet files. `LOCAL` or `S3` |
| `AWS_ACCESS_KEY_ID`    | String  |               | AWS Access Key to connect on S3 when using `STORAGE_TYPE` as `S3` |
| `AWS_SECRET_ACCESS_KEY`| String  |               | AWS Access Key ID to connect on S3 when using `STORAGE_TYPE` as `S3` |
| `AWS_SESSION_TOKEN`    | String  |               | AWS Session Token if necessary                 |
| `AWS_REGION`           | String  | `us-east-1`   | AWS region where S3 Bucket was created         |
| `AWS_BUCKET_NAME`      | String  |               | AWS S3 Bucket where parquet files are created  |
| `AWS_BUCKET_PREFIX`    | String  |               | AWS S3 Bucket prefix directory where parquet files are created  |
| `REPROCESS`            | Bool    | `False`       | If `True`, all processed file will be reprocessed |

## Accessing Grafana
After processing the files, you can access Grafana at:

http://localhost:3000

Use the following credentials:

- Username: admin
- Password: password


## AWS Action Required

### Reading Monthly Files

The CUR (Cost and Usage Reports) processor is configured to read only files under `AWS_BUCKET_PREFIX` path in Parquet format. It specifically looks for files within the `AWS_BUCKET_PREFIX` directory in the specified S3 bucket. After processing, the files will be renamed with the `.processed` extension.

### Configuring CUR v2 in Parquet on AWS

To enable Cost and Usage Report (CUR) v2 in Parquet format and configure the data export to an S3 bucket, follow these steps:

1. **Access the AWS Console**:
   - Log in to your AWS account.
   - Navigate to the **Billing and Cost Management** service.

2. **Create a Cost and Usage Report**:
   - In the navigation pane, click on **Data Exports**.
   - Click the **Create** button and choose **Standard data export**

3. **Configure the Report**:
   - Name your report, for example, `monthly-cost-usage-report`.
   - Check the **Include resource IDs** option to get detailed information.
   - On **Time granularity**, select **Monthly**
   - On **Format** use **Parquet - Parquet**

4. **Configure Report Delivery**:
   - Select an existing S3 bucket or create a new bucket where the report will be stored.
   - Ensure the directory structure in the S3 bucket is set to `reports/` for the data export configuration.
   - Click **Next**.

5. **Set Report Path**:
   - Set the S3 report path prefix to `reports/`.
   - Ensure the path is correctly set to store reports in the desired directory.

6. **Review and Complete**:
   - Review your settings.
   - Click **Save and complete** to finish the setup.

Once the CUR is configured and active, the processor will read the monthly Parquet files from the `reports/` directory in the S3 bucket for processing.

Follow these instructions to set up, run, and manage the AWS Cur V2 Processor. Ensure your environment meets the prerequisites and that you follow the steps in the correct order.