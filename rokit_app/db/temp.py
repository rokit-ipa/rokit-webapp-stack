import os
import influxdb_client
from fastapi import HTTPException
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


query_api = client.query_api()


def read_influxdb():
    results = []
    query = f'from(bucket: "{bucket}") |> range(start: -30m)'
    result = query_api.query(org=org, query=query)
    for table in result:
        for record in table.records:
            results.append((record.get_field(), record.get_value()))
    return results

print(read_influxdb())


