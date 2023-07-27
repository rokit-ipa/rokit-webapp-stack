#!/usr/bin/env python3
import uvicorn
from fastapi import FastAPI
from database import read_influxdb

app = FastAPI()
results = read_influxdb.read()

@app.get('/')
def read_root():
    return {"message": "OK"}

if __name__ == '__main__':
    uvicorn.run(f"{Path(__file__).stem}:app", host="localhost", port=8000, reload=True)