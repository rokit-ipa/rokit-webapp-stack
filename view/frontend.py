from fastapi import FastAPI
from nicegui import app, ui
import matplotlib
import numpy

from database import read_influxdb

TABS = ["Run a Test", "View and Edit the Test", "Testcases Protocol Guidelines"]
TESTCASES_LIST = ["MAX_VELOCITY", "MAX_VELOCITY_SLOPE", "BREAKING_DISTANCE"]
TRACKER_OBJECT_LIST = ["rokit_1", "rokit_2"]

def init(fastapi_app: FastAPI) -> None:
    
    def get_db_readings(): 
        results = read_influxdb.read()
        return results; 
    
    def set_test_parameters():
        print("here")


    @ui.page('/main')
    def show():

        ui.label('Rokit Testing Application').classes('text-h4')

        with ui.tabs() as tabs:
            for tab in TABS: 
                ui.tab(tab)

        with ui.footer(value=False) as footer:
            ui.label('Footer')


        with ui.page_sticky(position='bottom-right', x_offset=20, y_offset=20):
            ui.button(on_click=footer.toggle, icon='contact_support').props('fab')

        with ui.tab_panels(tabs, value=TABS[0]).classes('w-1/5'):
            with ui.tab_panel('Run a Test'):
                ui.label('Testcase Configuration').classes('text-h5')
                ui.element('div').classes('p-2 bg-white-100')
                ui.label('Choose a testcase...')
                with ui.element('div').classes('p-2 bg-blue-100'):
                    select1 = ui.select(TESTCASES_LIST, value=TESTCASES_LIST[0])
                ui.label('Choose the tracking object...')
                radio1 = ui.radio(TRACKER_OBJECT_LIST, value=TRACKER_OBJECT_LIST[0]).props('inline')
                ui.label('Test Protocol Notes...')
                ui.textarea(label='Text', placeholder='start typing',
                    on_change=lambda e: result.set_text('you typed: ' + e.value))
                result = ui.label()
                
            with ui.tab_panel(TABS[1]):
                print(get_db_readings())
                data = get_db_readings()
                with ui.pyplot(figsize=(3, 2)):
                    print(data)
                    x = numpy.linspace(data[0][1], data[1][1], data[2][1])
                    y = numpy.log(x)
                    matplotlib.pyplot.title('Velocity Graph')
                    matplotlib.pyplot.plot(x, y, '-')
            with ui.tab_panel(TABS[2]):
                ui.label('')



    ui.run_with(
        fastapi_app,
        storage_secret='pick your private secret here',  # NOTE setting a secret is optional but allows for persistent storage per user
    )