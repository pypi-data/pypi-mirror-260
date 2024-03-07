from pydantic import BaseModel

class energy_analysis_input(BaseModel):
    id: int
    name: str
    description: str = None
    city: str