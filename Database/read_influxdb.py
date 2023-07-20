import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

def read(): 
    token = "_6i-0rzenVKTsLYWGBjZ5St7SYZBE_cCeHEk8AcPe0fD1zSNZK5FboxGes5D4NRCGohR5QOsqwkV9ZlBqSEHQQ=="
    org = "IPA"
    bucket = "rokit-db"
    # Store the URL of your InfluxDB instance
    url="http://localhost:8086"

    client = influxdb_client.InfluxDBClient(
        url=url,
        token=token,
        org=org
    )
    results = []

    #Query operation 
    query_api = client.query_api()
    query = 'from(bucket:"rokit-db")\
    |> range(start: -30m)\
    |> filter(fn:(r) => r.test_case == "max_vel")'
    result = query_api.query(org=org, query=query)
    print(result)
    for table in result:
        for record in table.records:
            results.append((record.get_field(), record.get_value()))
    return results
