## Imports 
import pygal
import requests
from datetime import datetime
import webbrowser

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
    
    # Build URL
    url = (f"https://www.alphavantage.co/query?function={time_function}"
           f"&symbol={stock_symbol}&apikey={API_KEY}&outputsize=full&datatype=json")
    
    #variables
    api_response = requests.get(url)
    
    # Check if the request was successful by comparing to 200
    if api_response.status_code == 200:
        stock_data = api_response.json()  

        # Get the time series data based on the time function
        time_type = {
            "TIME_SERIES_DAILY": "Time Series (Daily)",
            "TIME_SERIES_WEEKLY": "Weekly Time Series",
            "TIME_SERIES_MONTHLY": "Monthly Time Series"
        }.get(time_function, None)

        if not time_type:
            print("Time function not supported for filtering.")
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
    
## Function to generate chart
def generate_chart(data, chart_type, stock_symbol):
    # Create the chart based on user input
    chart = pygal.Bar(title=f"{stock_symbol} Stock Prices") if chart_type == "1" else pygal.Line(title=f"{stock_symbol} Stock Prices")
    
    # Add data to the chart
    dates = sorted(data.keys())
    closing_prices = [float(data[date]['4. close']) for date in dates]
    
    chart.x_labels = dates
    chart.add(stock_symbol, closing_prices)
    
    # Save chart to file and open in browser
    chart_file = f"{stock_symbol}_stock_chart.svg"
    chart.render_to_file(chart_file)
    webbrowser.open(chart_file)

## Function to validate date input
def validate_date(date_text):
    try:
        return datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        return None
    

## Main program
if __name__ == "__main__":
    print("Stock Data Visualizer")
    print("-----------------------")

    # Validate stock symbol input
    stock_symbol = input("Enter the stock symbol you are looking for: ").upper()

    while not stock_symbol.isalnum():
        print("Invalid stock symbol. Please try again.")
        stock_symbol = input("Enter the stock symbol you are looking for: ").upper()

    # Ask for chart type
    print("\nChart Types\n-------------\n1. Bar\n2. Line")
    chart_type = input("Enter the chart type you want (1, 2): ")

    while chart_type not in ["1", "2"]:
        print("Invalid chart type, please try again.")
        chart_type = input("Enter the chart type you want (1, 2): ")

    # Ask for time series
    print("\nSelect the Time Series of the chart you want to Generate")
    print("----------------------------------------------------------")
    print("1. Daily\n2. Weekly\n3. Monthly")
    time_series_option = input("Enter time series option (1, 2, 3): ")

    time_series_map = {
        "1": "TIME_SERIES_DAILY",
        "2": "TIME_SERIES_WEEKLY",
        "3": "TIME_SERIES_MONTHLY"
    }

    while time_series_option not in time_series_map:
        print("Invalid time series option, please try again.")
        time_series_option = input("Enter time series option (1, 2, 3): ")

    time_function = time_series_map[time_series_option]

    # Ask for start date and end date
    beginning_date = input("Enter the start date (YYYY-MM-DD): ")
    while not validate_date(beginning_date):
        print("Invalid date format, please try again.")
        beginning_date = input("Enter the start date (YYYY-MM-DD): ")

    ending_date = input("Enter the end date (YYYY-MM-DD): ")
    while not validate_date(ending_date) or datetime.strptime(ending_date, '%Y-%m-%d') < datetime.strptime(beginning_date, '%Y-%m-%d'):
        print("Invalid end date or end date is before start date, please try again.")
        ending_date = input("Enter the end date (YYYY-MM-DD): ")

    # Retrieve stock data
    stock_data = retrieve_stock_data(stock_symbol, time_function, beginning_date, ending_date)

    # If data is retrieved successfully, generate the chart
    if stock_data:
        generate_chart(stock_data, chart_type, stock_symbol)
    else:
        print("No data available for the given stock symbol and date range.")
    