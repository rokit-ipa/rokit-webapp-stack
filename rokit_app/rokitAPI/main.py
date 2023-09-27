#!/usr/bin/env python3
import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from datetime import datetime, timedelta
from rokit_app.rokitAPI.models import TestParameters, TestResults
from rokit_app import frontend
from rokit_app.db.influxdb_helper import write_influxdb, read_influxdb
from rokit_app.db.database import create_test_results, SessionLocal, TestResultsDB

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

@app.post("/store_results/")
def write_results(results: TestResults):
    create_test_results(results)
    return {"message": "Data inserted successfully"}

@app.get("/get_results/")
def read_results():
    db = SessionLocal()
    results = db.query(TestResultsDB).all()
    db.close()
    return [{"trial": result.trial_number,
            "test name": result.test_name, 
            "robot name": result.robot_name,
            "temperature": result.temperature,
            "humidity": result.humidity,
            "inclination": result.inclination,
            "floor_type": result.floor_type,
            "tracking_object": result.tracking_object,
            "notes": result.notes,
            "velocity": result.velocity}
        for result in results]



frontend.init(app)



