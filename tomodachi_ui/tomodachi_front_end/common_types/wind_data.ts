export interface WindDataInput {
  Timestamp: string;
  Wind_Speed: number;
  Wind_Gust: number;
  Wind_Direction: number;
  Temperature: number;
  Humidity: number;
  Precipitation: number;
  Pressure: number;
  Cloud_Cover: number;
  Solar_Radiation: number;
  Hour_of_Day: number;
  Day_of_Week: number;
  Month: number;
  Wind_Speed_Squared: number;
  Wind_Speed_Cubed: number;
}

// for form input (drop Timestamp if not needed)
export type WindDataForm = Omit<WindDataInput, "Timestamp">;

// to send prediction request
export type PredictionRequest = Pick<WindDataInput, 
  "Wind_Speed" | "Wind_Gust" | "Wind_Direction" | "Temperature" |
  "Humidity" | "Precipitation" | "Pressure" | "Cloud_Cover" |
  "Solar_Radiation" | "Hour_of_Day" | "Day_of_Week" | "Month"
>; 


// Removed:
// Wind_Speed_Squared: number;
// Wind_Speed_Cubed: number;

export type PythonModelResponseType = {
  "xgboost_prediction": number;
  "random_forest_prediction": number;
  "linear_regression_prediction": number;
  "gradient_boosting_prediction": number;
}