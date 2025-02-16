import os
import requests
from dotenv import load_dotenv
import geocoder

class WeatherService:
    """Handles weather-related API requests and data processing."""
    
    def __init__(self):
        """Initializes the WeatherService class."""
         
        load_dotenv()
        self.api_key = os.getenv('WEATHER_API_KEY')
        self.base_url = os.getenv('WEATHER_API_BASE_URL')

    def get_weather(self):
        """Fetches weather data for a given city."""
        
        print("Fetching weather data...")
        params = {
            'q': self.__get_city(),
            'appid': self.api_key,
            'units': 'metric'
        }
        response = requests.get(self.base_url, params=params, timeout=10)
        if response.status_code == 200:
            weather = response.json().get("weather")
            return weather[0].get("main")
        else:
            response.raise_for_status()
            
    def __get_city(self): 
        g = geocoder.ip('me')
        if g.ok:
            print(f"City: {g.city}")
            return g.city
        else:
            return "City not found"
        

# Example usage:
# weather_service = WeatherService()
# weather_data = weather_service.get_weather('London')
# print(weather_data)