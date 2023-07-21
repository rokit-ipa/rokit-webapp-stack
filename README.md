# RoKit testing stack
-------------------------------------------------------------------------

**1.** Run the influxDB on the hostmachine
   ```
   docker-compose  -f docker-compose-influxdb.yaml up --build
   ```
-------------------------------------------------------------------------

**2.** Setup InfluxDB. 
   1. Copy the token from the influxDB dashboard 
   2. Organisation - IPA
   3. Bucket -  rokit-db 
   4. Set a username & password
-------------------------------------------------------------------------
**3.**  Add these setup details to the `.env` files in the `database` directory

-------------------------------------------------------------------------

**4.** Write some dummy data into the influxDB to start testing your application
   ```
   py Database/write_influxdb.py
   ```
-------------------------------------------------------------------------

**5.** Start FastAPI with uvicorn which also launches the nicegui
   ```
   uvicorn  view.rokitAPI.main:app --reload --host localhost --port 8000
   ```

-------------------------------------------------------------------------
###### Note: report issues in the GitHub issues.
-------------------------------------------------------------------------
