import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

def read(): 
    token = "BJoVKfcew0nl2yZ1QgJYhO2J03Pqo37FrGpjuoGPFB6nLbQJyrSmnu_AblLSQPcl6b5_cP9YjSREBQWIw9CYHw=="
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
