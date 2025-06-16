from tomodachi_core.models.demographic_salary_model.demographic_salary_model import DemographicSalaryModel
from tomodachi_core.models.weather_impact_model.weather_impact_model_semen import WeatherImpactModel


# The features of our dataset are:
feature_map = {
    "T-WG": ("Wind_Gust", "Temperature"),           # Wind Gust x Temperature
    "H-WG": ("Wind_Gust", "Humidity"),              # Wind Gust x Humidity
    "CC-WG": ("Wind_Gust", "Cloud_Cover"),          # Wind Gust x Cloud Cover
    "SR-WG": ("Wind_Gust", "Solar_Radiation"),      # Wind Gust x Solar Radiation
    "T-WS": ("Wind_Speed", "Temperature"),          # Wind Speed x Temperature
    "H-WS": ("Wind_Speed", "Humidity"),             # Wind Speed x Humidity
    "CC-WS": ("Wind_Speed", "Cloud_Cover"),         # Wind Speed x Cloud Cover
    "SR-WS": ("Wind_Speed", "Solar_Radiation"),     # Wind Speed x Solar Radiation
}

