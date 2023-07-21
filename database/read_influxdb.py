import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import os
from dotenv import load_dotenv, find_dotenv




def read(): 
    load_dotenv(find_dotenv())
    token =  os.environ.get("")


    token = os.environ.get("INFLUXDB_TOKEN")
    org = os.environ.get("INFLUXDB_ORG")
    bucket = os.environ.get("INFLUXDB_BUCKET")
    url=os.environ.get("INFLUXDB_URL")  

    client = influxdb_client.InfluxDBClient(
        url=url,
        token=token,
        org=org
    )
    results = []

    #Query operation 
    query_api = client.query_api()
    query = 'from(bucket:"rokit-db")\
    |>range(start: -90d)\
    |> filter(fn:(r) => r.test_case == "max_vel")'
    result = query_api.query(org=org, query=query)
    print(result)
    for table in result:
        for record in table.records:
            results.append((record.get_field(), record.get_value()))
    return results
