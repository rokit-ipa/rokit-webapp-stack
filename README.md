# RoKit testing stack
-------------------------------------------------------------------------

**1.** Run the influxDB on the hostmachine
   ```
   docker-compose  -f docker-compose up --build
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
###### Note: report issues in the GitHub issues.
-------------------------------------------------------------------------
