import os
import random
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from dotenv import load_dotenv, find_dotenv


class writeInfluxDB():
    def __init__(self) -> None:
        load_dotenv(find_dotenv())
        self.token = os.environ.get("INFLUXDB_TOKEN")
        self.org = os.environ.get("INFLUXDB_ORG")
        self.bucket = os.environ.get("INFLUXDB_BUCKET")
        self.url = os.environ.get("INFLUXDB_URL")       
        self.client = influxdb_client.InfluxDBClient(
            url=self.url,
            token=self.token,
            org=self.org,
            bucket=self.bucket)
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)

    def writePoints(self):
        for _ in range(1000):
            vel1=random.randint(40, 45)
            vel2=random.randint(35, 40)
            vel3=random.randint(30, 40)
            
            p = influxdb_client.Point("test_2").tag("test_case", "max_vel").field("velocity1", vel1).field("velocity2", vel2).field("velocity3", vel3)
            
            self.write_api.write(bucket=self.bucket, org=self.org, record=p)
        print("Successfully wrote some dummy data to InfluxDB")


def main():
    write_db = writeInfluxDB()
    write_db.writePoints()

if __name__ == "__main__":
    main()