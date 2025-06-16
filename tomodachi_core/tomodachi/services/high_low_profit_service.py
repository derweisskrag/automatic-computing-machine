"""
Author: Alexander
Colloborated: Sergei

Date: 2023-10-03
Description: HighLowProfit class for analyzing energy production data.

This module provides the `HighLowProfit` class for analyzing energy production data,
specifically identifying and summarizing periods of high and low profitability.

Key functionalities:
- Compute mean and standard deviation for selected energy metrics
- Classify time-series data into 'High', 'Low', or 'Normal' profitability periods
- Detect continuous periods of high and low returns
- Generate summary statistics for each detected period
- Enable a full analysis pipeline via a single `run_analysis()` method

Intended for use with pandas DataFrames containing time-indexed measurements of
energy output, wind speed, temperature, humidity, or other relevant metrics.

Example columns expected: ['Power_Output', 'Wind_Speed', 'Temperature', 'Humidity']

"""


from typing import Union
import pandas as pd
from numpy import select

# Removed (object)
class HighLowProfit:
    """
    Class for analysis of energy production data.
    Finds periods of high and low returns based on statistical analysis.
    """

    # Use DataFrame instead of path - Exposed to PandasService
    def __init__(self, df: pd.DataFrame) -> None:
        assert df is not None, "DataFrame cannot be None"
        self._df = df.copy()


    def print_info(self) -> None:
        print(f"""
        Mean Output: {self.mean_output}\n
        Std Output: {self.std_output}\n
        High Threshold: {self.high_threshold}\n
        Low Threshold: {self.low_threshold}\n""")


    def print_periods(self) -> None:
        print(f"""
        High Periods: {self.high_periods}\n
        Low Periods: {self.low_periods}\n""")


    def calculate_statistics(self, columns: list[str] = 'Power_Output') -> pd.DataFrame:
        """
        Calculate mean, standard deviation, and high/low thresholds for a specified column.
        Stores results in attributes: mean_output, std_output, high_threshold, low_threshold.

        Parameters:
        column (str): Column in DataFrame to compute statistics for.

        Returns:
        pd.DataFrame: Original DataFrame (or optionally, a copy).
        """

        # define the stats
        stats = self._df[columns].agg(['mean', 'std'])
        self.mean_output = stats['mean']
        self.std_output = stats['std']

        # Compute high and low thresholds
        self.high_threshold = self.mean_output + self.std_output
        self.low_threshold = self.mean_output - self.std_output

        # Possible return itself or df
        return self
    

    def classify_data(self, columns: Union[list[str], str] = 'Power_Output') -> pd.DataFrame:
        """
        Classification of data for periods of high, low and normal profitability.
        """
        if self.mean_output is None or self.std_output is None:
            raise ValueError('First you need to calculate the statistics')

        # compute conditions and choices
        conditions = [
            (self._df[columns] > self.high_threshold),
            (self._df[columns] < self.low_threshold)
        ]

        choices = ['High', 'Low']
        self._classify_data_with_conditions(conditions, choices)
        return self
    

    def _classify_data_with_conditions(self, conditions: list, choices: list) -> pd.DataFrame:
        self._df['Status'] = select(conditions, choices, default='Normal')
    
    
    def find_periods(self) -> pd.DataFrame:
        """
        Search for continuous periods of high and low profitability using vectorized operations.
        """
        if 'Status' not in self._df.columns:
            raise ValueError('First you need to classify the statistics')

        self.high_periods = self._find_periods_of_status_vectorized('High')
        self.low_periods = self._find_periods_of_status_vectorized('Low')
        return self


    def _find_periods_of_status_vectorized(self, status) -> list[tuple]:
        # define the mask for the desired status
        mask = self._df['Status'] == status
        shifted = mask.shift(fill_value=False)
        edges = mask != shifted
        group_id = edges.cumsum()

        # Filter to only groups that are True (i.e., status == desired status)
        mask_groups = mask.groupby(group_id)

        periods = []
        for key, val in mask_groups:
            if val.iloc[0]:  # Only interested in groups where status == True
                indices = val.index
                periods.append((indices[0], indices[-1] + 1))  # end-exclusive

        return periods

    def create_periods_dataframe(self, columns: list[str] = ['Power_Output', 'Wind_Speed', 'Temperature', 'Humidity']) -> pd.DataFrame:
        """
        Generate a DataFrame with summary stats for periods of high and low profitability.
        """
        if not self.high_periods and not self.low_periods:
            raise ValueError('You need to find the periods first.')


        high_stats = self._summarize_periods(columns, self.high_periods, 'High')
        low_stats = self._summarize_periods(columns, self.low_periods, 'Low')

        df_summary = pd.DataFrame(high_stats + low_stats)
        return df_summary.sort_values('Start Time')
    
    
    def process_period(self):
        self._df['Production_Level'] = 'Normal'
        for start, end in self.high_periods:
            self._df.loc[start:end, 'Production_Level'] = 'High'

        for start, end in self.low_periods:
            self._df.loc[start:end, 'Production_Level'] = 'Low'
        return self._df


    def _summarize_periods(self, columns, periods, label) -> list[dict]:
        summaries = []
        for start, end in periods:
            data = self._df.loc[start:end]
            stats = {
                'Period Type': label,
                'Start Time': start,
                'End Time': end,
                'Duration Hours': len(data),
            }
            for col in columns:
                if col in data.columns:
                    stats[f'Avg_{col}'] = data[col].mean()
                    stats[f'Max_{col}'] = data[col].max()
                    stats[f'Min_{col}'] = data[col].min()
            summaries.append(stats)
        return summaries
    

    def run_analysis(self, columns) -> dict:
        """
        Function, that runs all processes.
        """
        
        hlp = (
            HighLowProfit(self._df)
            .calculate_statistics(columns)
            .classify_data(columns)
            .find_periods()
        )

        results = {
            'mean_output': hlp.mean_output,
            'std_output': hlp.std_output,
            'high_threshold': hlp.high_threshold,
            'low_threshold': hlp.low_threshold,
            'high_periods': hlp.high_periods,
            'low_periods': hlp.low_periods,
            'periods_df': hlp._df
        }

        return results