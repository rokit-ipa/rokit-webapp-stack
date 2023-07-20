# Test_Kit
1. Setup InfluxDB. You need a token, organisation and bucket. Adapt the files read_database and write_database with your token,organisation and bucket. 
   
   ```
   docker run --name influxdb -d -p 8086:8086 --volume `pwd`/influxdb2:/var/lib/influxdb2 --volume `pwd`/config.yml:/etc/influxdb2/config.yml influxdb:2.0.7
   ```

   ```
   docker exec influxdb influx setup \
    --bucket rokit-db \
    --org IPA \
    --password qwertz1234 \
    --username rar \
    --force

   ```
   
   ```
   py Database/write_influxdb.py
   ```
2. Start FastAPI with uvicorn 
   ```
   uvicorn FastAPI.main:app --reload
   ```
