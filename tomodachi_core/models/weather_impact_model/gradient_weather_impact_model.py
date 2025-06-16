from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import r2_score, root_mean_squared_error
import joblib


class TomodachiGradientModel(BaseEstimator, RegressorMixin):
    def __init__(self, 
                 n_estimators=100, 
                 learning_rate=0.1, 
                 max_depth=3, 
                 random_state=42,
                 save_to_path="gradient_model.joblib"):
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.random_state = random_state
        self.save_to_path = save_to_path
        self.model = GradientBoostingRegressor(
            n_estimators=self.n_estimators,
            learning_rate=self.learning_rate,
            max_depth=self.max_depth,
            random_state=self.random_state
        )
    

    def fit(self, X, y):
        self.model.fit(X, y)
        preds = self.model.predict(X)
        r2 = r2_score(y, preds)
        rmse = root_mean_squared_error(y, preds)
        print(f"GradientBoostingRegressor fit complete!")
        print(f"Training R2 score: {r2:.4f}")
        print(f"Training RMSE: {rmse:.4f}")

        return self  # important for sklearn compatibility
    
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
    
    # Optional: expose parameters for hyperparameter tuning
    def get_params(self, deep=True):
        return {
            "n_estimators": self.n_estimators,
            "learning_rate": self.learning_rate,
            "max_depth": self.max_depth,
            "random_state": self.random_state,
        }
    
    def set_params(self, **params):
        for key, val in params.items():
            setattr(self, key, val)
        # Recreate the underlying model with new params
        self.model = GradientBoostingRegressor(
            n_estimators=self.n_estimators,
            learning_rate=self.learning_rate,
            max_depth=self.max_depth,
            random_state=self.random_state
        )
        return self

