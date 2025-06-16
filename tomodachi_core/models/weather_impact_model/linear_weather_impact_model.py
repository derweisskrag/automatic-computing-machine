"""
Linear Regression Model to predict Power Output (y)
based on features X.

This example model is designed for team training.

Assumption: Input data is already preprocessed (e.g., imputation, scaling)
before being passed to this model.
"""


from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import root_mean_squared_error, r2_score
import joblib


class TomodachiLinearRegressionModel:
    def __init__(self):
        self.model = LinearRegression()

    def fit(self, X, y):
        """
        Fits a single Linear Regression model on the whole dataset.
        """
        self.model.fit(X, y)
        preds = self.model.predict(X)
        r2 = r2_score(y, preds)
        rmse = root_mean_squared_error(y, preds)
        print(f"LinearRegression fit complete!")
        print(f"Training R2 score: {r2:.4f}")
        print(f"Training RMSE: {rmse:.4f}")
        return self
        

    def predict(self, X):
        return self.model.predict(X)
    
    def save(self, path=None):
        path = path or self.save_to_path
        joblib.dump(self.model, path)
        print(f"Model saved to {path}")
    
    def load(self, path=None):
        path = path or self.save_to_path
        self.model = joblib.load(path)
        print(f"Model loaded from {path}")
        return self
    
    def log_errors(self, y_true, y_pred):
        print("R2 score:", r2_score(y_true, y_pred))
        print("RMSE:", root_mean_squared_error(y_true, y_pred))
    

    def get_params(self, deep=True):
        return {
            "n_estimators": self.n_estimators,
            "learning_rate": self.learning_rate,
            "max_depth": self.max_depth,
            "random_state": self.random_state
        }
    
    def set_params(self, **params):
        for key, val in params.items():
            setattr(self, key, val)
        # Recreate the underlying model with new params
        self.model = LinearRegression(
            n_estimators=self.n_estimators,
            learning_rate=self.learning_rate,
            max_depth=self.max_depth,
            random_state=self.random_state
        )
        return self


