#!/usr/bin/env python3
import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from datetime import datetime, timedelta
from rokit_app.rokitAPI.models import TestParameters, TestResults
from rokit_app import frontend
from rokit_app.db.influxdb_helper import write_influxdb, read_influxdb, read_influxdb_query

app = FastAPI()


@app.get('/')
async def read_index():
    return FileResponse('rokit_app/static/index.html')

@app.post('/setparams')
def set_params(params: TestParameters):
    return write_influxdb(params)

@app.get('/getparams')
def get_params():
    # start_time = (datetime.now() - timedelta(days=1)).isoformat()  # 1 day ago
    # end_time = datetime.now().isoformat()
    # measurement = "MAX_VELOCITY"
    # data = read_influxdb_query(measurement, start_time, end_time)
    # return data
    return read_influxdb()


@app.post('/storeresults')
def store_results():
    pass

@app.get('/getresults')
def get_results():
    pass



frontend.init(app)



