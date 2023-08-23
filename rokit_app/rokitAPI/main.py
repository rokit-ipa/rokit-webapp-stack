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
    pass

@app.get('/getparams')
def get_params():
    pass

@app.post('/storeresults')
def store_results(request: TestResults):
    return write_influxdb(request)

@app.get('/getresults')
def get_results():
    return read_influxdb()

frontend.init(app)



