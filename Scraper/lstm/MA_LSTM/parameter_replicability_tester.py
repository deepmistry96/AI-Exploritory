import os
import pandas as pd

def process_files(folder_path):
    results = {}
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r') as file:
                lines = file.readlines()
            
            i = 0
            while i < len(lines):
                if '10-day MA prediction after 5 days' in lines[i]:
                    params_line = lines[i-1].strip()
                    params = params_line.split(',')[1:6]  
                    param_key = tuple(params) 

                    prediction_line = lines[i].split(',')[1].strip()
                    try:
                        prediction = float(prediction_line)
                        if param_key not in results:
                            results[param_key] = []
                        results[param_key].append(prediction)
                    except ValueError:
                        print(f"Skipping invalid prediction format in file {filename}, line {i+1}")
                i += 3 

    if results:
        columns = ['Time Steps', 'Test Size', 'Dropout Rate', 'Units', 'Learning Rate'] + [f'Prediction {i+1}' for i in range(max(len(v) for v in results.values()))]
        data = []
        for key, values in results.items():
            row = list(key) + values
            data.append(row)
        return pd.DataFrame(data, columns=columns)
    else:
        return pd.DataFrame()

    ###can change this to be taken as input
folder_path = './parameter_comb_results/BYND_5_10_24/'

result_df = process_files(folder_path)

if not result_df.empty:
    ####can change the last part to be input based
    output_file = 'aggregated_predictions_BYND_5-10-24.csv'
    result_df.to_csv(output_file, index=False)
    print(f"Aggregated predictions saved to {output_file}")
else:
    print("No valid data to save.")
