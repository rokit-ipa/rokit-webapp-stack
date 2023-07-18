from fastapi import FastAPI
from nicegui import app, ui
import matplotlib
import numpy

from Database import read_influxdb

def init(fastapi_app: FastAPI) -> None:
    def get_db_readings(): 
        results = read_influxdb.read()
        return results; 


    @ui.page('/main')
    def show():
        ui.label('Rokit Testing Application')
        print(get_db_readings())
        # NOTE dark mode will be persistent for each user across tabs and server restarts
        ui.dark_mode().bind_value(app.storage.user, 'dark_mode')
        ui.checkbox('dark mode').bind_value(app.storage.user, 'dark_mode')
        data = get_db_readings()

        with ui.pyplot(figsize=(3, 2)):
            print(data)
            x = numpy.linspace(data[0][1], data[1][1], data[2][1])
            y = numpy.log(x)
            matplotlib.pyplot.title('Velocity Graph')
            matplotlib.pyplot.plot(x, y, '-')
    ui.run_with(
        fastapi_app,
        storage_secret='pick your private secret here',  # NOTE setting a secret is optional but allows for persistent storage per user
    )
