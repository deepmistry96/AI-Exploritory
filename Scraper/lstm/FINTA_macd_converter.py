import pandas as pd
from finta import TA

data = pd.DataFrame({
    'Open': [1, 2, 3, 4, 5],
    'High': [2, 3, 4, 5, 6],
    'Low': [1, 2, 3, 4, 5],
    'Close': [2, 3, 4, 5, 6],
    'Volume': [100, 150, 200, 250, 300]
})

try:
    macd = TA.MACD(data)
    print(macd)
except Exception as e:
    print("An error occurred:", e)
