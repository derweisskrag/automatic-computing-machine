"""
Utils functions for the high-low profit analysis.

"""

# Utils functions for the high-low profit analysis.
def analyze_power_profit(analyzer, save_results=True):
    # Assuming analyzer is an instance of HighLowProfit passed from the controller layer
    analyzer.load_data()
    analyzer.calculate_statistics()
    analyzer.classify_data()
    analyzer.find_periods()

    # similar to run_analysis() method in HighLowProfit
    if save_results:
        analyzer.save_results()

    # Return the results
    results = {
        'mean_output': analyzer.mean_output,
        'std_output': analyzer.std_output,
        'high_threshold': analyzer.high_threshold,
        'low_threshold': analyzer.low_threshold,
        'high_periods': analyzer.high_periods,
        'low_periods': analyzer.low_periods,
        'periods_df': analyzer.create_periods_dataframe(),
        'data_with_status': analyzer.df.reset_index()
    }

    return results

