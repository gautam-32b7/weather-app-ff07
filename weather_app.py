from dotenv import load_dotenv

import requests
import datetime
import os


# Load environment variable from .env file
load_dotenv()

class WeatherApp:
    def __init__(self):
        # Base URL for OpenWeatherMap API
        self.api_url = "http://api.openweathermap.org/data/2.5/weather"
        self.weather_history = []

    # Fetch the current weather for a city using OpenWeatherMap API
    def fetch_weather(self, city):
        params = {
            "q": city,
            "appid": os.getenv("API_KEY"),
            "units": "metric"
        }

        response = requests.get(self.api_url, params=params)
        if response.status_code == 200:
            data = response.json()
            weather = {
                "temperature": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "condition":data["weather"][0]["description"].capitalize()
            }
            return weather
        else:
            return None
        
    def display_weather(self, city):
        # Display weather and store it in history
        weather = self.fetch_weather(city)

        if weather:
            # Get the current timestamp
            current_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            print(f"Weather in {city} at {current_time}: ")
            print(f"Temperature: {weather['temperature']} C")
            print(f"Humidity: {weather['humidity']}%")
            print(f"Condition: {weather['condition']}")
            
            # store weather in history
            self.weather_history.append({
                "city":city,
                "time":current_time,
                "weather":weather.copy()
            })
        else:
            print(f"Sorry, weather data for {city} is unavailable")

    def show_weather_history(self):
        # Show all recorded weather history
        if self.weather_history:
            print("\nWeather History")
            for entry in self.weather_history:
                print(f"{entry['time']} - {entry['city']}: {entry['weather']}")
        else:
            print("No weather history available")

# Main driver code
def main():
    app = WeatherApp()

    while True:
        print("\n--- Weather App ---")
        print("1. Get current weather")
        print("2. Show weather history")
        print("3. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            city = input("Enter city name: ")
            app.display_weather(city)
        elif choice == "2":
            app.show_weather_history()
        elif choice == "3":
            print("Exiting the app. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()