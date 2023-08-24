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
        .tag("robot_name", data.robot_name) \
        .tag("trial_number", data.trial_number) \
        .tag("tracking_object", data.tracking_object) \
        .tag("temperature", data.temperature) \
        .tag("humidity", data.humidity) \
        .tag("inclination", data.inclination) \
        .tag("floor_type", data.floor_type) \
        .tag("notes", data.notes) \
        .tag("velocity", data.velocity) 
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
    query = f'from(bucket: "rokit-db") \
            |> range(start: -1h)  \
            |> filter(fn: (r) => r["_measurement"] == "MAX_VELOCITY" )\
            |> filter(fn:(r) => r.robot_name == "MiR")'
    result = query_api.query(org=org, query=query)
    for table in result:
        for record in table.records:
            results.append((record.tag(), record.get_value()))
    return results

def read_influxdb_query(measurement, start_time, end_time):
    pass