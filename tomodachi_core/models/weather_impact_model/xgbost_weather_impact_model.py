import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import xgboost as xgb
from sklearn.metrics import r2_score, root_mean_squared_error
from tomodachi_core.common_types.result import Result, Ok, Err

class TomodachiXGBoost:
    """
    Wrapper for XGBoost Regressor with sklearn-compatible interface and
    Result-based error handling for training and prediction.

    Parameters:
    -----------
    X : pd.DataFrame or np.ndarray
        Feature data.
    y : pd.Series or np.ndarray
        Target data.
    """

    def __init__(self,):
        self.model = xgb.XGBRegressor(random_state=42)
        self.trained = False


    def fit(self, X, y, test_size=0.2, random_state=42):
        """
        Splits data, fits the XGBoost model, and logs performance on test set.

        Args:
            X (pd.DataFrame or np.ndarray): Feature data.
            y (pd.Series or np.ndarray): Target data.
            test_size (float): Fraction of data to hold out for testing.
            random_state (int): Seed for reproducibility.

        Returns:
            Ok(None) if successful, Err(Exception) if error occurs.
        """

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        self.model.fit(X_train, y_train)
        self.trained = True

        preds = self.model.predict(X_test)
        print("XGBoost training results:")
        self.log_errors(y_test, preds)

        return self


    def predict(self, X) -> np.typing.NDArray | Result[None, ValueError]:
        """
        Predict with the trained model. Returns Result wrapping predictions.
        """
        if not self.trained:
            return Err(ValueError("Model is not trained yet! Call fit() first."))

        return self.model.predict(X)
        
        
    def score(self, X, y) -> float:
        """
        Returns R2 score of the model on given data.

        Raises:
        -------
        ValueError if model not trained yet.
        """
        if not self.trained:
            raise ValueError("Model not trained. Call fit() before score.")
        
        preds = self.model.predict(X)
        return r2_score(y, preds)


    def log_errors(self, y_true, y_pred):
        """
        Logs R2 and RMSE to console.
        """
        print(f"R2 score: {r2_score(y_true, y_pred):.4f}")
        print(f"RMSE: {root_mean_squared_error(y_true, y_pred):.4f}")
