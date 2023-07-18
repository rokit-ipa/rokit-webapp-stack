import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS


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

# Write script
write_api = client.write_api(write_options=SYNCHRONOUS)

p = influxdb_client.Point("test_2").tag("test_case", "max_vel").field("velocity1", 40).field("velocity2", 15).field("velocity3", 13)
write_api.write(bucket=bucket, org=org, record=p)
print("Successfully wrote some datapoints to DB")
