import json
import boto3
import pandas as pd
from io import StringIO
from sqlalchemy import create_engine
import pymysql
import os

#S3 and RDS details: charlie puth - artist_data
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
S3_BUCKET = "spotify-fetch-data"
S3_FILE_KEY = "2025-02-18_Charlie Puth_data.csv"
DB_NAME = "initial_db"
DB_TABLE = "artist_data"

#Initialize S3 client
s3_client = boto3.client("s3")

def lambda_handler(event, context):
   #Read the CSV file from S3
   response = s3_client.get_object(Bucket=S3_BUCKET, Key=S3_FILE_KEY)
   csv_data = response["Body"].read().decode("utf-8")
  
   #Convert CSV data to Pandas DataFrame
   df = pd.read_csv(StringIO(csv_data))
   print(df)

   #Create SQLAlchemy database connection
   engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")
  
   #Write DataFrame to MySQL table (if_exists="append" will add data to existing table)
   df.to_sql(DB_TABLE, con=engine, if_exists="replace", index=False)
  
   return {
       "statusCode": 200,
       "body": json.dumps("Data successfully uploaded to MySQL!")
   }
