from matplotlib import pyplot as plt
from matplotlib import dates as mdates


def visualize_power_profit(input_data, columns, output_file="power_profit_visualization.png", show_plot=True):
    required_keys = ['periods_df', 'mean_output', 'high_threshold',
                     'low_threshold', 'high_periods', 'low_periods']
    
    for key in required_keys:
        if key not in input_data:
            raise ValueError(f"Required key {key} not found in input data")

    df = input_data['periods_df'].copy()
    if 'Timestamp' in df.columns:
        df.set_index('Timestamp', inplace=True)

    mean_output = input_data['mean_output']
    high_threshold = input_data['high_threshold']
    low_threshold = input_data['low_threshold']
    high_periods = input_data['high_periods']
    low_periods = input_data['low_periods']

    plt.figure(figsize=(15, 8))

    plt.plot(df.index, df[columns], label='Power Output', color='blue')


    plt.axhline(y=mean_output, color='green', linestyle='-', label=f'Mean: ({mean_output:.2f})')
    plt.axhline(y=high_threshold, color='red', linestyle='--', label=f'High profitability: ({high_threshold:.2f})')
    plt.axhline(y=low_threshold, color='orange', linestyle='--', label=f'Low profitability: ({low_threshold:.2f})')


    for start, end in high_periods:
        plt.axvspan(
            start,
            end,
            alpha=0.2,
            color='red',
            label='_' if 'High profitability' in plt.gca().get_legend_handles_labels()[1]
            else 'High profitability'
        )
    for start, end in low_periods:
        plt.axvspan(
            start,
            end,
            alpha=0.2,
            color='blue',
            label='_' if 'Low profitability' in plt.gca().get_legend_handles_labels()[1]
            else 'Low profitability'
        )

    plt.title('Power Output Analysis')
    plt.xlabel('Time')
    plt.ylabel('Power Output')
    plt.legend(loc='best')
    plt.grid(True)

    # plt.gca().xaxis.set_major_locator(mdates.DateFormatter('%Y-%m-%d %H'))
    # plt.gcf().autofmt_xdate()

    plt.tight_layout()
    plt.savefig(output_file)

    if show_plot:
        plt.show()
    else:
        plt.close()

    print(f"Visualization saved to: {output_file}")
