from pydantic import BaseModel

class energy_analysis_input(BaseModel):
    id: int
    name: str
    description: str = None
    city: str

class energy_analysis_output(BaseModel):
    parameter1: str
    parameter2: str