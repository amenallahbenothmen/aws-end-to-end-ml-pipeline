## Project Overview

The **Electric Power Consumption Forecasting System** is a fully operational machine learning pipeline designed to predict real-time electricity consumption. By leveraging historical data and integrating real-time data streams, the system provides accurate power consumption forecasts for multiple zones. The project incorporates time-series feature engineering, scalable deployment using AWS, and real-time visualization through Grafana, making it suitable for dynamic operational environments.
## Features

- **Real-Time Data Streaming**:Streams real-time data using AWS Kinesis Data Streams for continuous forecasting.
- **Electricity Usage Forecasting**:Utilizes advanced models, such as XGBoost, for accurate multi-zone power consumption predictions.
- **Time Series Feature Engineering**: Generates robust features to improve model accuracy and forecasting reliability.
- **AWS Cloud Integration**:Employs AWS services like S3 for model storage and Kinesis for real-time data ingestion and streaming.
- **Visualization with Grafana**: Provides interactive dashboards to monitor real-time power consumption trends and forecasting results.



## Prerequisites

- **Python 3.9** 
- **AWS CLI**
- **Grafana**

## Setup and Installation

Follow the steps below to set up and run the application:

### 1. Clone the Repository

```bash
git clone https://github.com/amenallahbenothmen/aws-end-to-end-ml-pipeline.git
cd aws-end-to-end-ml-pipeline

```

### 2.Create a Virtual Environment

```bash
conda create -n aws_pipeline python=3.9 -y
conda activate aws_pipeline
```


### 3.Install Dependencies

```bash
pip install -r requirements.txt
```


