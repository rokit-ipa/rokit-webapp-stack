from fastapi import FastAPI
from nicegui import ui

# Define the constants
conditions_file_path = "view/docs/conditions.md"
protocols_file_path = "view/docs/protocols.md"
TABS = ["Run Tests", "Results", "Test Protocols", "Test Conditions"]
INPUTS_PER_TAB = 3
INPUT_NAMES = ["Temperature (C)", "Humidity (%)", "Inclination(degrees)"]
DROPDOWN_OPTIONS = ["Option 1", "Option 2", "Option 3"]
TESTCASES_LIST = ["MAX_VELOCITY", "MAX_VELOCITY_SLOPE"]
TRACKER_OBJECT_LIST = ["rokit_1", "rokit_2"]


def init(fastapi_app: FastAPI) -> None:

    def read_markdown_file(file_path):
        with open(file_path, "r") as f:
            markdown_content = f.read()
        return markdown_content

    def set_background(color: str) -> None:
        ui.query('body').style(f'background-color: {color}')

    @ui.page('/ui')
    def view():
        # ui.dark_mode().bind_value(app.storage.user, 'dark_mode')
        # ui.checkbox('dark mode').bind_value(app.storage.user, 'dark_mode')
        with ui.header().classes(replace='row items-center') as header:
            with ui.tabs().classes('w-full justify-center') as tabs:
                for tab in TABS:
                    ui.tab(tab)

        with ui.footer(value=True) as footer:
            ui.label(
                'RoKit testing stack @ Fraunhofer IPA 2023').classes('absolute-center items-center')

        input_values = {}
        with ui.tab_panels(tabs):
            with ui.tab_panel(TABS[0]):
                ui.label('Configure the Test').classes('text-h4')
                with ui.card():
                    for input_name in INPUT_NAMES:
                        value = ui.input(input_name)
                        # this value has to be pushed to the database
                        input_values[input_name] = value

                with ui.card():
                    with ui.row():
                        ui.button('Save', on_click=lambda: ui.notify(
                            'Yay!', type='positive'))
                        ui.button('Start', on_click=lambda: ui.colors(
                            primary='#2bcf61'))
                        ui.button('Stop', on_click=lambda: ui.colors())
                with ui.left_drawer(value=True).classes('bg-blue-100') as left_drawer_0:
                    ui.label('Select Test')
                    with ui.element('div').classes('p-2 bg-blue-100'):
                        select0 = ui.select(
                            TESTCASES_LIST, value=TESTCASES_LIST[0])
                        print(str(select0))

            with ui.tab_panel(TABS[1]):
                ui.label('Test Results').classes('text-h4')

            with ui.tab_panel(TABS[2]):
                markdown_content = read_markdown_file(protocols_file_path)
                ui.markdown(markdown_content)

            with ui.tab_panel(TABS[3]):
                markdown_content = read_markdown_file(conditions_file_path)
                ui.markdown(markdown_content)

    ui.run_with(
        fastapi_app,
        # NOTE setting a secret is optional but allows for persistent storage per user
        storage_secret='pick your private secret here',
        title='Robot Testing Kit'
    )
