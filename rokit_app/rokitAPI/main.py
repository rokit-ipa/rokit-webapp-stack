#!/usr/bin/env python3
import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse

from rokit_app.rokitAPI.models import TestParameters, TestResults
from rokit_app import frontend
from rokit_app.db.influxdb_helper import write_influxdb, read_influxdb

app = FastAPI()


@app.get('/')
async def read_index():
    return FileResponse('rokit_app/static/index.html')

@app.post('/setparams')
def set_params(params: TestParameters):
    return write_influxdb(params)

@app.get('/getparams')
def get_params():
    return read_influxdb()

@app.post('/storeresults')
def store_results():
    pass

@app.get('/getresults')
def get_results():
    pass



frontend.init(app)



