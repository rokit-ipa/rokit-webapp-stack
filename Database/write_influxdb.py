import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import random

# You can generate a Token from the "Tokens Tab" in the UI
token = "_6i-0rzenVKTsLYWGBjZ5St7SYZBE_cCeHEk8AcPe0fD1zSNZK5FboxGes5D4NRCGohR5QOsqwkV9ZlBqSEHQQ=="
org = "IPA"
bucket = "rokit-db"

client = influxdb_client.InfluxDBClient(
    url="http://localhost:8086",
    token=token,
    org=org,
    bucket=bucket)


# Write script
write_api = client.write_api(write_options=SYNCHRONOUS)

for i in range(1000):
    vel1=random.randint(40, 65)
    vel2=random.randint(35, 49)
    vel3=random.randint(30, 51)
    p = influxdb_client.Point("test_2").tag("test_case", "max_vel").field("velocity1", vel1).field("velocity2", vel2).field("velocity3", vel3)
    write_api.write(bucket=bucket, org=org, record=p)
print("Successfully wrote some dummy data to InfluxDB")

