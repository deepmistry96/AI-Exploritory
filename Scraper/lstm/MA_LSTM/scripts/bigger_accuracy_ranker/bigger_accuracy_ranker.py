import os
import pandas as pd

def get_average_ranks(folder_path, output_file):
    all_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    rank_data = []

    for file in all_files:
        file_path = os.path.join(folder_path, file)
        df = pd.read_csv(file_path)
        
        for index, row in df.iterrows():
            p_comb = (row['Time Steps'], row['Test Size'], row['Dropout Rate'], row['Units'], row['Learning Rate'])
            rank_data.append({'Parameter Combination': p_comb, 'Rank': index + 1})
    
    rank_df = pd.DataFrame(rank_data)
    rank_df_grouped = rank_df.groupby('Parameter Combination')['Rank'].mean().reset_index()
    rank_df_grouped = rank_df_grouped.sort_values('Rank')
    
    rank_df_grouped.to_csv(output_file, index=False)

# Specify the path to your folder containing the CSV files and the output file path
folder_path = '/Users/calebm/AI-Exploritory/Scraper/lstm/MA_LSTM/parameter_comb_results/KO_runs/KO_ranks/overall_ranks'
output_file = '2best_parameter_combinations.csv'

get_average_ranks(folder_path, output_file)
print(f"Output file '{output_file}' has been created with the best parameter combinations.")
