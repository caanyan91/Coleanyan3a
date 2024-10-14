## Imports 
import pygal
import requests
from datetime import datetime

# Set API KEY
API_KEY = "K5MNQEQQ1D7IYJ0M"

## Retrieve stock data from alpha vantage function

def retrieve_stock_data(stock_symbol, time_function, beginning_date, ending_date):
    try:
        # Parse the dates
        start_date_input = datetime.strptime(beginning_date, "%Y-%m-%d")
        end_date_input = datetime.strptime(ending_date, "%Y-%m-%d")
        
        # exception handling check if the end date is before the start date
        if end_date_input < start_date_input:
            raise ValueError("Start date must be before end date.")
    
    except ValueError as e:
        # exception handling invalid date format error
        print("Invalid format for date entered. Please use the format YYYY-MM-DD.")
        return None
    
    # string concantenation to build url
    # make sure data type is set to data type being used, also nmake sure outputsize is set to full
    url = "https://www.alphavantage.co/query?function=" + time_function + "&symbol=" + stock_symbol + "&apikey=" + API_KEY + "&outputsize=full&datatype=json"
    
    #variables
    api_response = requests.get(url)
    
# Check if the request was successful by comparing to 200
    if api_response.status_code == 200:
        stock_data = api_response.json()  

        # Get the time series data based on the time function
        if time_function == "TIME_SERIES_DAILY":
            time_type = "Time Series (Daily)"
        elif time_function == "TIME_SERIES_WEEKLY":
            time_type = "Weekly Time Series"
        elif time_function == "TIME_SERIES_MONTHLY":
            time_type = "Monthly Time Series"
        else:
            print("Time function not supported for filtering")
            return None
        
        time_series_data = stock_data.get(time_type, {})
        
        # Exception handling for data range
        date_range_data = {date: values for date, values in time_series_data.items() if beginning_date <= date <= ending_date}
        
        if not date_range_data:
            print(f"No data found between {beginning_date} and {ending_date}. Please choose valid date range")
            return None
        
        return date_range_data
    else:
        print(f"Failed to retrieve data. HTTP Status Code: {api_response.status_code}")
        return None
    
    