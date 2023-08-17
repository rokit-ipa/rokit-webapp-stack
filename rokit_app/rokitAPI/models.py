from pydantic import BaseModel


class TestParameters(BaseModel):
    test_name: str
    temperature: float
    humidity: float
    inclination: float
    floor_type: str
    notes: str

class TestResults(BaseModel):
    trial: int
    velocity: float