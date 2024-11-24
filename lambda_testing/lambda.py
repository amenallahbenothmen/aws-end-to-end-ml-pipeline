import json
import boto3
import base64
import sys
import os


sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import xgboost as xgb
import numpy as np
from xgboost import DMatrix


s3_client = boto3.client('s3')
bucket_name = 'energiemodel'


def lambda_handler(event, context):
    try:
        print("Event received:", json.dumps(event))  

        records = event.get('Records', [])
        print(f"Number of records: {len(records)}")  

        model = load_model()

        for record in records:
            try:
                print(f"Processing record: {record}")  

                payload = base64.b64decode(record['kinesis']['data'])
                print(f"Decoded payload: {payload}")  

                kinesis_data = json.loads(payload)
                print(f"Kinesis data: {kinesis_data}") 

                processed_data, feature_vector, s3_key_data, s3_key_result = process_data(kinesis_data)
                print(f"Processed data: {processed_data}, feature_vector: {feature_vector}, s3_key_data: {s3_key_data}, s3_key_result: {s3_key_result}")

                prediction = predict(model, [feature_vector])

                result = {
                    "PowerConsumption_Zone1": prediction[0],
                    "PowerConsumption_Zone2": prediction[1],
                    "PowerConsumption_Zone3": prediction[2],
                    "hour": processed_data["hour"],  
                    "minute": processed_data["minute"],  
                    "month": processed_data["month"], 
                    "day": processed_data["day"],  
                    "year": processed_data["year"]   
                }

                s3_client.put_object(
                    Bucket=bucket_name,
                    Key=s3_key_data,
                    Body=json.dumps(processed_data),
                    ContentType='application/json'
                )
                print(f"Data successfully written to S3: {s3_key_data}")

                s3_client.put_object(
                    Bucket=bucket_name,
                    Key=s3_key_result,
                    Body=json.dumps(result),
                    ContentType='application/json'
                )
                print(f"Results successfully written to S3: {s3_key_result}")

            except Exception as record_error:
                print(f"Error processing record: {record}. Error: {record_error}")

        return {
            'statusCode': 200,
            'body': json.dumps("Data processed and stored successfully in S3.")
        }

    except Exception as e:
        print(f"Error in lambda_handler: {e}") 
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error processing data: {str(e)}")
        }


def load_model():
    try:
        s3_file_path = 'models/xgb_model.json'  
        local_model_path = '/tmp/xgb_model.json'  # Temporary location for the lambda function


        s3_client.download_file(bucket_name, s3_file_path, local_model_path)
        print("Model downloaded from S3.")


        model = xgb.Booster()
        model.load_model(local_model_path)
        print("Model loaded successfully.")
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        raise
 

def predict(model, input_data):
    try:
        feature_names = ['Temperature', 'Humidity', 'WindSpeed', 'GeneralDiffuseFlows', 'DiffuseFlows', 'hour', 'minute', 'dayofweek', 'quarter', 'month', 'day', 'year', 'season', 'dayofyear', 'dayofmonth', 'weekofyear', 'is_weekend', 'is_month_start', 'is_month_end', 'is_quarter_start', 'is_quarter_end', 'is_working_day', 'is_business_hours', 'is_peak_hour', 'minute_of_day', 'minute_of_week']

        dmatrix = DMatrix(np.array(input_data), feature_names=feature_names)

        predictions = model.predict(dmatrix)
        print(f"Raw Predictions: {predictions}")

        # Flatten predictions
        if len(predictions.shape) == 2:  # Check if it's a 2D array
            predictions = predictions[0]  
        print(f"Flattened Predictions: {predictions}")

        return predictions.tolist()  
    except Exception as e:
        print(f"Error during prediction: {e}")
        raise



def process_data(data):
    Date_time = data.get("Datetime", "unknown_date")  


    processed_data = {
        "Temperature": data.get("Temperature", None),
        "Humidity": data.get("Humidity", None),
        "WindSpeed": data.get("WindSpeed", None),
        "GeneralDiffuseFlows": data.get("GeneralDiffuseFlows", None),
        "DiffuseFlows": data.get("DiffuseFlows", None),
        "hour": data.get("hour", None),
        "minute": data.get("minute", None),
        "dayofweek": data.get("dayofweek", None),
        "quarter": data.get("quarter", None),
        "month": data.get("month", None),
        "day": data.get("day", None),
        "year": data.get("year", None),
        "season": data.get("season", None),
        "dayofyear": data.get("dayofyear", None),
        "dayofmonth": data.get("dayofmonth", None),
        "weekofyear": data.get("weekofyear", None),
        "is_weekend": data.get("is_weekend", None),
        "is_month_start": data.get("is_month_start", None),
        "is_month_end": data.get("is_month_end", None),
        "is_quarter_start": data.get("is_quarter_start", None),
        "is_quarter_end": data.get("is_quarter_end", None),
        "is_working_day": data.get("is_working_day", None),
        "is_business_hours": data.get("is_business_hours", None),
        "is_peak_hour": data.get("is_peak_hour", None),
        "minute_of_day": data.get("minute_of_day", None),
        "minute_of_week": data.get("minute_of_week", None)
    }


    feature_vector = [
        processed_data.get("Temperature", 0),
        processed_data.get("Humidity", 0),
        processed_data.get("WindSpeed", 0),
        processed_data.get("GeneralDiffuseFlows", 0),
        processed_data.get("DiffuseFlows", 0),
        processed_data.get("hour", 0),
        processed_data.get("minute", 0),
        processed_data.get("dayofweek", 0),
        processed_data.get("quarter", 0),
        processed_data.get("month", 0),
        processed_data.get("day", 0),
        processed_data.get("year", 0),
        processed_data.get("season", 0),
        processed_data.get("dayofyear", 0),
        processed_data.get("dayofmonth", 0),
        processed_data.get("weekofyear", 0),
        processed_data.get("is_weekend", 0),
        processed_data.get("is_month_start", 0),
        processed_data.get("is_month_end", 0),
        processed_data.get("is_quarter_start", 0),
        processed_data.get("is_quarter_end", 0),
        processed_data.get("is_working_day", 0),
        processed_data.get("is_business_hours", 0),
        processed_data.get("is_peak_hour", 0),
        processed_data.get("minute_of_day", 0),
        processed_data.get("minute_of_week", 0)
    ]



    s3_key_data = f"test/{Date_time}.json"
    s3_key_result = f"results/{Date_time}.json"

    return processed_data, feature_vector, s3_key_data, s3_key_result



