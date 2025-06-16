import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import r2_score


class WeatherImpactModel:
    """
    The linear regression model for prediction Power Output based on all features

    """
    def __init__(self, df: pd.DataFrame = None, csv_file_path: str = None):
        self.csv_file_path = csv_file_path
        self.df = None
        self.model = None
        self.feature_names = None
        self.feature_importances = None


    # for machine learning (formulas)
    # A/B tests
    def adding_groups(self):
        self.df['T-WG'] = self.df['Wind_Gust']*self.df['Temperature'] # Wind Gust x Temperature
        self.df['H-WG'] = self.df['Wind_Gust']*self.df['Humidity'] # Wind Gust x Humidity
        self.df['CC-WG'] = self.df['Wind_Gust']*self.df['Cloud_Cover'] # Wind Gust x Cloud Cover
        self.df['SR-WG'] = self.df['Wind_Gust']*self.df['Solar_Radiation'] # Wind Gust x Solar Radiation
        self.df['T-WS'] = self.df['Wind_Speed']*self.df['Temperature'] # Wind Speed x Temperature
        self.df['H-WS'] = self.df['Wind_Speed']*self.df['Humidity'] # Wind Speed x Humidity
        self.df['CC-WS'] = self.df['Wind_Speed']*self.df['Cloud_Cover'] # Wind Speed x Cloud Cover
        self.df['SR-WS'] = self.df['Wind_Speed']*self.df['Solar_Radiation'] # Wind Speed x Solar Radiation
        
    

    # Model creation 
    # NB! Our data is
    def create_model(self, check_r2_score=True):
        X = self.df[['T-WG', 'H-WG', 'CC-WG', 'SR-WG', 'T-WS', 'H-WS', 'CC-WS', 'SR-WS']]
        y = self.df['Power_Output']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model = GradientBoostingRegressor(random_state=42)
        self.model.fit(X_train, y_train)
        if check_r2_score:
            y_pred = self.model.predict(X_test)
            r2 = r2_score(y_test, y_pred)

            print(f"R²: {r2:.3f}")

    def get_results(self):
        self.feature_names = self.model.feature_names_in_
        self.feature_importances = self.model.feature_importances_

    def save_results(self, output_csv="weather_condition_importances.csv"):
        feature_df = pd.DataFrame({
            "Feature": self.feature_names,
            "Importance": self.feature_importances
        })
        feature_df.to_csv(output_csv, index=False)
        return feature_df  # Optional: return it for further use


    def visualize(self, output_png="results.png"):
        sorted_idx = np.argsort(self.feature_importances)[::-1]

        plt.figure(figsize=(10, 6))
        sns.barplot(x=self.feature_importances[sorted_idx], y=self.feature_names[sorted_idx], palette='viridis')
        plt.title('Feature Importance in GradientBoostingRegressor Model')
        plt.xlabel('Significance')
        plt.ylabel('Feature')
        
        plt.grid(True)
        plt.tight_layout()

        plt.savefig(output_png)
        plt.show()


    def run_analysis(self, save_results=True, visualize=True):
        self.load_data()
        self.adding_groups()
        self.create_model(check_r2_score=True) # If R² > 0.8 - model works very good
        self.get_results()

        if save_results:
            self.save_results()
        if visualize:
            self.visualize()

        if len(self.feature_names) != len(self.feature_importances):
            raise ValueError
        results = {name: imp for name, imp in zip(self.feature_names, self.feature_importances)}

        return results