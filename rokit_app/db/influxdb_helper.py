import os
import influxdb_client
from fastapi import FastAPI, HTTPException
from datetime import datetime
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client.client.query_api import QueryApi
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())
token = os.environ.get("INFLUXDB_TOKEN")
org = os.environ.get("INFLUXDB_ORG")
bucket = os.environ.get("INFLUXDB_BUCKET")
url = os.environ.get("INFLUXDB_URL")
client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org,
    bucket=bucket)
write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()

def write_influxdb(data):
    point = influxdb_client.Point(data.test_name)  \
        .field("trial_number", data.trial_number) \
        .field("robot_name", data.robot_name) \
        .field("tracking_object", data.tracking_object) \
        .field("temperature", data.temperature) \
        .field("humidity", data.humidity) \
        .field("inclination", data.inclination) \
        .field("floor_type", data.floor_type) \
        .field("velocity", data.velocity) \
        .field("notes", data.notes)
    try:
        write_api.write(bucket=bucket, org=org, record=point)
        response = {"message": "Data logged to the db"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        client.close()

    return response

def read_influxdb():
    results = []
    query = 'from(bucket:"rokit-db")\
            |> range(start: -30m)'
    result = query_api.query(org=org, query=query)
    for table in result:
        for record in table.records:
            results.append((record.get_field(), record.get_value()))
    return results

def read_influxdb_query(measurement, start_time, end_time):
    query_api = client.query_api()

    query = f'from(bucket: "{bucket}") \
        |> range(start: {start_time}, stop: {end_time}) \
        |> filter(fn: (r) => r["_measurement"] == "{measurement}")'

    try:
        result = query_api.query(org=org, query=query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))