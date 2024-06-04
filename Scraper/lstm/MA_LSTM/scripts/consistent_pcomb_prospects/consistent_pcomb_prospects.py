import pandas as pd
#input: a csv file with every parameter combination and its predicted prices as input

#process: reads into a folder and iterates through every file
#process: through every file, groups predictions according to parameter combinations
#process: creates a master list of all reasonable parameter combinations
#process: if predictions are ____% (tolerance number) away from any of the other predictions, that parameter combination is taken off the master list
#process: if a p.comb has <= 1 prediction price, that p.comb is still stored in the master list

#output: a csv file with a list of parameter combinations that are "consistent" after multiple runs

def filter_predictions(csv_path):
    df = pd.read_csv(csv_path)
    
    def is_consistent(row):
        predictions = [row[f'Prediction {i+1}'] for i in range(len(row) - 5) if pd.notna(row[f'Prediction {i+1}'])]
        if len(predictions) < 2:
            return True 
        max_pred = max(predictions)
        min_pred = min(predictions)
        return (max_pred - min_pred) / max_pred <= 0.0025  #tolerance number
    consistent_df = df[df.apply(is_consistent, axis=1)]
    
    parameter_columns = ['Time Steps', 'Test Size', 'Dropout Rate', 'Units', 'Learning Rate']
    filtered_df = consistent_df[parameter_columns]
    #change output_path accordingly 
    output_path = 'consistent_parameters.csv'
    filtered_df.to_csv(output_path, index=False)
    print(f"Consistent parameter combinations saved to {output_path}")

#change path accordingly
csv_path = '/Users/calebm/AI-Exploritory/Scraper/lstm/MA_LSTM/parameter_comb_results/BYND_5_10_24/results/aggregated_predictions_BYND_5-10-24.csv'  # Change this to your actual CSV file path
filter_predictions(csv_path)
