import requests
import datetime as dt

def get_baltic_electricity_prices():
    """Get Baltic electricity prices for today"""
    today = dt.datetime.today()
    end_datetime = today.strftime("%Y-%m-%dT23:00Z")
    start_datetime = today.strftime("%Y-%m-%dT00:00Z") 

    # Get raw data from Elering API
    api_url = "https://dashboard.elering.ee/api/nps/price"
    response = requests.get(
        url=api_url, 
        params={"start":start_datetime, "end":end_datetime}
        ).json()

    return response