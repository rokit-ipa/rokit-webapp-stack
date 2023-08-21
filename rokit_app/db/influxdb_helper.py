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

def write_influxdb(data):
    point = influxdb_client.Point(data.test_name)  \
        .field("trial_number", data.trial_number) \
        .field("tracking_object", data.tracking_object) \
        .field("temperature", data.temperature) \
        .field("humidity", data.humidity) \
        .field("inclination", data.inclination) \
        .field("floor_type", data.floor_type) \
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
    query = f'from(bucket: "{bucket}") |> range(start: -3h) |> filter(fn: (r) => r._measurement == "MAX_VELOCITY")'
    result = client.query_api().query(org=org, query=query)   
    # data = []
    # for table in result:
    #     for record in table.records:
    #         data.append({
    #             "test_name": record.values["_field"],
    #             "temperature": record.values["temperature"],
    #             "humidity": record.values["humidity"],
    #             "inclination": record.values["inclination"],
    #             "floor_type": record.values["floor_type"],
    #             "notes": record.values["notes"]
    #         })
    # return data
    return result

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