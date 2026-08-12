"""
Random Forest model for checking out our thing
"""
from sklearn.ensemble import RandomForestRegressor
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.metrics import root_mean_squared_error, r2_score

class TomodachiForestModel(BaseEstimator, RegressorMixin):
    def __init__(self, n_estimators=100, random_state=42):
        self.n_estimators = n_estimators
        self.random_state = random_state
        self.model = RandomForestRegressor(n_estimators=self.n_estimators, random_state=self.random_state)
        
    def fit(self, X, y):
        self.model.fit(X, y)
        preds = self.model.predict(X)
        r2 = r2_score(y, preds)
        rmse = root_mean_squared_error(y, preds)
        print(f"RandomForestRegressor fit complete!")
        print(f"Training R2 score: {r2:.4f}")
        print(f"Training RMSE: {rmse:.4f}")
        return self
    

    def predict(self, X):
        return self.model.predict(X) 
    

    def get_params(self, deep=True):
        return {"n_estimators": self.n_estimators, "random_state": self.random_state}
    

    def set_params(self, **params):
        for key, val in params.items():
            setattr(self, key, val)
        self.model = RandomForestRegressor(n_estimators=self.n_estimators, random_state=self.random_state)
        return self



