#!/usr/bin/env python3
from View import frontend
from fastapi import FastAPI
from Database import read_influxdb

app = FastAPI()

results = read_influxdb.read()
print(results)

@app.get('/')
def read_root():
    return {'Hello': 'World'}

if __name__ == '__main__':
    frontend.init(app)
    print('Please start the app with the "uvicorn" command as shown in the start.sh script')