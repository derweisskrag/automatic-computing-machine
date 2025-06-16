"""
The model for demographic salary

Learning the machine learning model for salary prediction based on demographic data.
This model uses Gradient Boosting Regressor to predict salary based on age, city, and occupation.

"""


import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
import seaborn as sns

class DemographicSalaryModel:
    def __init__(self, data):
        self.raw_data = data
        self.df = pd.DataFrame(data)
        self.model = None
        self.feature_names = None
        self.feature_importances = None
        self.preprocessor = None

    def preprocess(self):
        X = self.df.drop(columns=["name", "salary"])
        y = self.df["salary"]

        categorical_features = ["city", "occupation"]
        numeric_features = ["age"]

        self.preprocessor = ColumnTransformer(
            transformers=[
                ('cat', OneHotEncoder(drop='first'), categorical_features),
                ('num', 'passthrough', numeric_features)
            ]
        )

        X_processed = self.preprocessor.fit_transform(X)
        self.feature_names = self.preprocessor.get_feature_names_out()

        return X_processed, y

    def train_model(self):
        X, y = self.preprocess()
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        self.model = GradientBoostingRegressor(random_state=42)
        self.model.fit(X_train, y_train)

        y_pred = self.model.predict(X_test)
        print(f"R²: {r2_score(y_test, y_pred):.3f}")

    def get_feature_importance(self):
        if not self.model:
            raise RuntimeError("Train the model first.")

        self.feature_importances = self.model.feature_importances_

        return dict(zip(self.feature_names, self.feature_importances))

    def visualize(self):
        if self.feature_importances is None:
            self.get_feature_importance()

        sorted_idx = np.argsort(self.feature_importances)[::-1]
        sorted_features = np.array(self.feature_names)[sorted_idx]
        sorted_importances = self.feature_importances[sorted_idx]

        plt.figure(figsize=(10, 5))
        sns.barplot(x=sorted_importances, y=sorted_features, palette="coolwarm")
        plt.title("Feature Importance for Salary Prediction")
        plt.xlabel("Importance")
        plt.ylabel("Feature")
        plt.tight_layout()
        plt.grid(True)
        plt.show()