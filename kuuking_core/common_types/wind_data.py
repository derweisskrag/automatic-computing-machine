from dataclasses import dataclass
from pydantic import BaseModel
from typing import Optional

@dataclass
class WindData:
    pass

class WindDataInput(BaseModel):
    # Timestamp: str  # or datetime if you parse it
    Wind_Speed: float
    Wind_Gust: float
    Wind_Direction: float
    Temperature: float
    Humidity: float
    Precipitation: float
    Pressure: float
    Cloud_Cover: float
    Solar_Radiation: float
    Hour_of_Day: int
    Day_of_Week: int
    Month: int
    Wind_Speed_Squared: float
    Wind_Speed_Cubed: float
    # Power_Output is excluded because it's the prediction target
    # Precipitation_Unit is also excluded unless used for prediction