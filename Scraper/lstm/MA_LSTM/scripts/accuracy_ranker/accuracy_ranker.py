import os
import pandas as pd

#How can we tell which P.combs (Parameter combinations) are accurate in predicting the actual 10 day MA?
#Answer: this script!!!

#input: folder with prediction results for every P.comb files inside 

#process: grouping and splitting parameters and predictions
#process: average the prediction price for each seperate P.comb
#process: find the distance of that prediction price from the actual price (think it should be line 57)
#process: rank these distances

#output: a csv file that contains distances & P.combs ranked from closes to the actual price to the farthest


def process_files(folder_path, target_price):
    results = {}
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r') as file:
                lines = file.readlines()
            
            i = 0
            while i < len(lines) - 1:
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
        data = []
        for key, values in results.items():
            average_prediction = sum(values) / len(values)
            distance = abs(average_prediction - target_price)
            data.append(list(key) + [average_prediction, distance])

        df = pd.DataFrame(data, columns=['Time Steps', 'Test Size', 'Dropout Rate', 'Units', 'Learning Rate', 'Average Prediction', 'Distance'])
        df.sort_values('Distance', inplace=True)
        return df
    else:
        return pd.DataFrame()
folder_path = '/Users/calebm/AI-Exploritory/Scraper/lstm/MA_LSTM/parameter_comb_results/KO_runs/KO_6_15_23'  #change this path as necessary

#change the actual price accordingly
result_df = process_files(folder_path, 60.71)

if not result_df.empty:
    #change output file accordingly
    output_file = 'KO_6-15-23_ranked_predictions.csv'
    result_df.to_csv(output_file, index=False)
    print(f"Ranked predictions saved to {output_file}")
else:
    print("No valid data to save.")
