"""
This is the main model of the Tomodachi for prediction 'Wind_Power'

It encompasses all other models and lets you predict the values in the best way.

This is the model used in the FastAPI.

Predict will work on unknown data as long as i feed the df that has the same columns but different nums (but types are correct), 
meaning that all i have to do is make them work, and use joblib to export them to a path. 
"""

import sys
import traceback
import joblib
import pathlib

# For magic method
from sklearn.ensemble import VotingRegressor
from sklearn.impute import SimpleImputer
from sklearn.model_selection import GridSearchCV, RepeatedStratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression

import pandas as pd
import numpy as np

from sklearn.metrics import (
    r2_score,
    root_mean_squared_error
)

from tomodachi_core.models.weather_impact_model import (
    TomodachiLinearRegressionModel,
    TomodachiGradientModel,
    TomodachiForestModel,
    TomodachiXGBoost
)


from tomodachi_core.common_types.result import (
    Result,
    Ok,
    Err,
    result_wrapper
)

# for extending
from sklearn.base import BaseEstimator, RegressorMixin


from sklearn.base import BaseEstimator, RegressorMixin

class TomodachiModel(BaseEstimator, RegressorMixin):
    """
    This is the main model of Tomodachi for predicting 'Wind_Power'.
    It encompasses all other models and provides a unified interface.
    """

    def __init__(self):
        self.linear_model = TomodachiLinearRegressionModel()
        self.gradient_model = TomodachiGradientModel()
        self.forest_model = TomodachiForestModel()
        self.xgboost_model = TomodachiXGBoost()
        self.voting_regressor = None

    def fit(self, X, y):
        self.linear_model.fit(X, y)
        self.gradient_model.fit(X, y)
        self.forest_model.fit(X, y)
        self.xgboost_model.fit(X, y)

        self._initialize_voting_regressor()
        self.voting_regressor.fit(X, y)

        y_pred = self.voting_regressor.predict(X)
        self.evaluate_model("VotingRegressor", y, y_pred)

        return self  

    def predict(self, X):
        if self.voting_regressor is None:
            raise RuntimeError("Model not fitted yet. Call 'fit' first.")
        return self.voting_regressor.predict(X)

    def _initialize_voting_regressor(self):
        self.voting_regressor = VotingRegressor(
            estimators=[
                ("lr", self.linear_model.model),
                ("rf", self.forest_model.model),
                ("gb", self.gradient_model.model),
                ("xgb", self.xgboost_model.model),
            ]
        )


    def save(self, path: str) -> Result[None, Exception]:
        try:
            path_obj = pathlib.Path(path)
            path_obj.parent.mkdir(parents=True, exist_ok=True)
            joblib.dump(self, path)
            return Ok(None)
        except Exception as e:
            return Err(error=e)


    def evaluate_model(self, model_name, y_true, y_pred):
        r2 = r2_score(y_true, y_pred)
        rmse = np.sqrt(root_mean_squared_error(y_true, y_pred))
        print(f"{model_name} R²: {r2:.4f}")
        print(f"{model_name} RMSE: {rmse:.4f}")
        return r2, rmse


    def hyper_tuning(self) -> Result[dict, Exception]:
        """
        Perform hyperparameter tuning using GridSearchCV on:
        - Linear Regression
        - Random Forest
        - Gradient Boosting
        - XGBoost
        
        Returns:
            Result containing dictionary with best estimators.
        """
        try:
            # Store tuned models
            tuned_models = {}

            # Define parameter grids
            param_grids = {
                'linear': {
                    'fit_intercept': [True, False],
                    'positive': [True, False]
                },
                'random_forest': {
                    'n_estimators': [50, 100],
                    'max_depth': [None, 10, 20],
                    'min_samples_split': [2, 5]
                },
                'gradient_boosting': {
                    'n_estimators': [50, 100],
                    'learning_rate': [0.01, 0.1],
                    'max_depth': [3, 5]
                },
                'xgboost': {
                    'n_estimators': [50, 100],
                    'learning_rate': [0.01, 0.1],
                    'max_depth': [3, 5]
                }
            }

            # Tuning Linear Regression
            linear_grid = GridSearchCV(
                estimator=self.linear_model.model,
                param_grid=param_grids['linear'],
                cv=5,
                scoring='r2',
                n_jobs=-1
            )
            linear_grid.fit(self.X, self.y)
            tuned_models['linear'] = linear_grid.best_estimator_

            # Tuning Random Forest
            rf_grid = GridSearchCV(
                estimator=self.forest_model.model,
                param_grid=param_grids['random_forest'],
                cv=5,
                scoring='r2',
                n_jobs=-1
            )
            rf_grid.fit(self.X, self.y)
            tuned_models['random_forest'] = rf_grid.best_estimator_

            # Tuning Gradient Boosting
            gb_grid = GridSearchCV(
                estimator=self.gradient_model.model,
                param_grid=param_grids['gradient_boosting'],
                cv=5,
                scoring='r2',
                n_jobs=-1
            )
            gb_grid.fit(self.X, self.y)
            tuned_models['gradient_boosting'] = gb_grid.best_estimator_

            # Tuning XGBoost
            xgb_grid = GridSearchCV(
                estimator=self.xgboost_model.model,
                param_grid=param_grids['xgboost'],
                cv=5,
                scoring='r2',
                n_jobs=-1
            )
            xgb_grid.fit(self.X, self.y)
            tuned_models['xgboost'] = xgb_grid.best_estimator_

            return Ok(tuned_models)

        except Exception as e:
            # Capture full traceback for easier debugging
            traceback_str = traceback.format_exc()
            print(f"Hyperparameter tuning failed:\n{traceback_str}")
            return Err(e)


    @staticmethod
    def save_models(models: dict, path: str) -> Result[None, Exception]:
        """
        Save trained models to the specified directory.

        Args:
            models (dict): Dictionary of trained models.
            path (str): Directory path to save the models.

        Returns:
            Result[None, Exception]: Ok(None) on success, Err(Exception) on failure.
        """
        try:
            output_dir = pathlib.Path(path)
            output_dir.mkdir(parents=True, exist_ok=True)  # Create the directory if it doesn't exist

            for name, model in models.items():
                model_filename = output_dir / f"{name}_model.pkl"
                joblib.dump(model, model_filename)
                print(f"Model '{name}' saved at: {model_filename}")

            return Ok(None)

        except Exception as e:
            import traceback
            traceback_str = traceback.format_exc()
            print(f"Failed to save models:\n{traceback_str}")
            return Err(e)

