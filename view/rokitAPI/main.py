#!/usr/bin/env python3
import uvicorn
from fastapi import FastAPI
from view import frontend

app = FastAPI()

@app.get('/')
def read_root():
    return {"message": "OK"}

frontend.init(app)

if __name__ == '__main__':
    uvicorn.run(f"{Path(__file__).stem}:app", host="localhost", port=8000, reload=True) 
