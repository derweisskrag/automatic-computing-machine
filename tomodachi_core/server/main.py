from tomodachi_core.common_types.wind_data import WindDataInput
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from contextlib import asynccontextmanager
import matplotlib.pyplot as plt


model_pipeline = None
import seaborn as sns


@asynccontextmanager
async def lifespan(app: FastAPI):
    root_dir = Path(__file__).parent.parent.parent.resolve()
    # model_path = root_dir / "shared" / "data" / "export" / "best_model_experiment_8.joblib"
    # app.state.model_pipeline = joblib.load(model_path)
    # print(f"✅ Model loaded from {model_path}")

    xgb_path = root_dir / "shared" / "data" / "export" / "xgb_model.joblib"
    rf_path = root_dir / "shared" / "data" / "export" / "rf_model.joblib"
    lr_path = root_dir / "shared" / "data" / "export" / "lr_model.joblib"
    gr_path = root_dir / "shared" / "data" / "export" / "gb_model.joblib"

    # # Load each model and store in app.state
    app.state.model_pipelines = {
        "xgb": joblib.load(xgb_path),
        "rf": joblib.load(rf_path),
        "lr": joblib.load(lr_path),
        "gr": joblib.load(gr_path)
    }

    print(f"✅ All models loaded from:")
    print(f"  XGB: {xgb_path}")
    print(f"  RF:  {rf_path}")
    print(f"  LR:  {lr_path}")
    print(f"  GR:  {gr_path}")
    yield


app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/predict/")
def predict_endpoint(input_data: WindDataInput, request: Request):
    # Convert Pydantic to DataFrame
    df = pd.DataFrame([input_data.model_dump()])

    # Add the runtime features
    df["Hour_of_Day_sin"] = np.sin(2 * np.pi * df["Hour_of_Day"] / 24)
    df["Hour_of_Day_cos"] = np.cos(2 * np.pi * df["Hour_of_Day"] / 24)
    df["Wind_Speed_12h_avg"] = df["Wind_Speed"]  # Dummy - since you don't have historical context in POST
    df["Wind_Gust_Diff"] = df["Wind_Gust"] - df["Wind_Speed"]
    df["Radiation_Lag1"] = df["Solar_Radiation"]  # Dummy - no past step, set to current

    # Drop columns the model doesn't need
    df = df.drop(columns=["Hour_of_Day"])

    # Predict
    models = app.state.model_pipelines


    # model_pipeline = request.app.state.model_pipeline
    # prediction = model_pipeline.predict(df)

    # return {"prediction": float(prediction[0])}

    prediction_xgb = models["xgb"].predict(df)[0]
    prediction_rf = models["rf"].predict(df)[0]
    prediction_lr = models["lr"].predict(df)[0]
    prediction_gr = models["gr"].predict(df)[0]

    return {
        "xgboost_prediction": float(prediction_xgb),
        "random_forest_prediction": float(prediction_rf),
        "linear_regression_prediction": float(prediction_lr),
        "gradient_boosting_prediction": float(prediction_gr)
    }



@app.get("/predict-all/")
def predict_all():
    root_dir = Path(__file__).parent.parent.parent.resolve()
    path_to_csv = (root_dir / "shared" / "data" / "processed" / "cleaned_Synthetic_Wind_Power.csv").resolve()
    output_dir = root_dir / "shared" / "data" / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(str(path_to_csv))

    X = df.drop(columns=["Power_Output", "Precipitation_Unit", "Timestamp"])
    y = df["Power_Output"]

    # Add the runtime features
    df["Hour_of_Day_sin"] = np.sin(2 * np.pi * df["Hour_of_Day"] / 24)
    df["Hour_of_Day_cos"] = np.cos(2 * np.pi * df["Hour_of_Day"] / 24)
    df["Wind_Speed_12h_avg"] = df["Wind_Speed"]  # Dummy - since you don't have historical context in POST
    df["Wind_Gust_Diff"] = df["Wind_Gust"] - df["Wind_Speed"]
    df["Radiation_Lag1"] = df["Solar_Radiation"]  # Dummy - no past step, set to current

    # Drop columns the model doesn't need
    df = df.drop(columns=["Hour_of_Day"])

    models = app.state.model_pipelines
    
    prediction_xgb = models["xgb"].predict(X)[0]
    prediction_rf = models["rf"].predict(X)[0]
    prediction_lr = models["lr"].predict(X)[0]
    prediction_gr = models["gr"].predict(X)[0]


    predictions = {}
    # Predict and plot residuals for each model
    for model_name, model in models.items():
        y_pred = model.predict(X)
        residuals = y - y_pred

        # Save residual plot
        plt.figure(figsize=(8, 6))
        sns.residplot(x=y_pred, y=residuals, lowess=True, color="blue", line_kws={"color": "red", "lw": 2})
        plt.xlabel("Predicted Power Output")
        plt.ylabel("Residuals")
        plt.title(f"Residual Plot - {model_name.upper()}")
        plt.axhline(0, linestyle='--', color='gray')
        plot_path = output_dir / f"residuals_{model_name}.png"
        plt.savefig(plot_path)
        plt.close()
        print(f"Residual plot saved to {plot_path}")

        # Save first prediction (single value) for display
        predictions[f"{model_name}_prediction"] = float(y_pred[0])

    return predictions
