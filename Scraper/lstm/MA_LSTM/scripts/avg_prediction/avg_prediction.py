import csv

# Function to calculate average of predictions
def calculate_average_predictions(file_path):
    predictions = []
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if row['Average Prediction']:
                predictions.append(float(row['Average Prediction']))
    if predictions:
        average_prediction = sum(predictions) / len(predictions)
        return average_prediction
    else:
        return None

# Specify the path to your CSV file
file_path = '/Users/calebm/AI-Exploritory/Scraper/lstm/MA_LSTM/parameter_comb_results/KO_runs/KO_ranks/overall_ranks/KO_6-15-23_ranked_predictions.csv'

# Calculate and print the average
average = calculate_average_predictions(file_path)
if average is not None:
    print(f"The average of all predictions is: {average}")
else:
    print("No predictions found in the file.")
