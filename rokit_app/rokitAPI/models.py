from pydantic import BaseModel


class TestParameters(BaseModel):
    test_name: str = ''
    trial_number: int = 0
    tracking_object: str = ''
    temperature: float = 0.0
    humidity: float = 0.0
    inclination: float = 0.0
    floor_type: str = ''
    notes: str = ''


class TestResults(BaseModel):
    trial: int = 0
    velocity: float = 0.0
