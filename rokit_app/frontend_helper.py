
from rokit_app.rokitAPI.models import TestParameters, TestResults

payload = TestParameters() 

def update_trial_number(value):
    payload.trial_number=value  

def update_temperature(value):
    payload.temperature=value       

def update_humidity(value):
    payload.humidity=value

def update_notes(value):
    payload.notes=value

def update_inclination(value):
    payload.inclination=float(value)

def update_floor_type(value):
    payload.floor_type=value

def update_test_name(value):
    payload.test_name = value
    return payload.test_name

def update_robot_name(value):
    payload.robot_name=value 


def update_tracking_object(value):
    payload.tracking_object=value 