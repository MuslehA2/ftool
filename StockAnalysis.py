import requests
import pandas as pd
import matplotlib.pyplot as plt
from Api_key2 import Api_Key2  # API key from professor


class StockAnalysis:
    def __init__(self, symbol):
        #stock ticker and API key
        self.symbol = symbol.upper()
        self.api_key = Api_Key2
        self.company_name = "N/A"
        self.current_price = "N/A"
        self.historical_data = None

    def get_company_details(self):
        #company's name and details
        url = "https://api.polygon.io/v3/reference/tickers/" + self.symbol + "?apiKey=" + self.api_key
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            details = data.get("results", {})
            self.company_name = details.get("name", self.company_name)
        else:
            print("Error getting company details\n")

    def get_latest_stock_price(self):
        #Get the latest stock price
        url = "https://api.polygon.io/v2/aggs/ticker/" + self.symbol + "/prev?adjusted=true&apiKey=" + self.api_key
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [{}])[0]
            self.current_price = results.get("c", self.current_price)  # Use the close price
        else:
            print("Error getting stock price\n")

    def fetch_historical_data(self, start_date, end_date):
        #Get the historical stock data
        url = (
            "https://api.polygon.io/v2/aggs/ticker/" + self.symbol + "/range/1/day/"
            + start_date + "/" + end_date + "?adjusted=true&sort=asc&apiKey=" + self.api_key
        )
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            if results:
                self.historical_data = pd.DataFrame(results)
                self.historical_data["Date"] = pd.to_datetime(self.historical_data["t"], unit="ms")
                self.historical_data.rename(
                    columns={"c": "Close", "h": "High", "l": "Low", "o": "Open", "v": "Volume"},
                    inplace=True
                )
                return True
            else:
                print("No data available for the date range\n")
                return False
        else:
            print("Error getting historical data\n")
            return False

   
