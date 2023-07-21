#!/usr/bin/env python3
from view import frontend
from fastapi import FastAPI
from database import read_influxdb

app = FastAPI()

results = read_influxdb.read()

@app.get('/')
def read_root():
    return {'Hello': 'World'}

if __name__ == '__main__':
    print('Please start the app with the "uvicorn" command as shown in the start.sh script')