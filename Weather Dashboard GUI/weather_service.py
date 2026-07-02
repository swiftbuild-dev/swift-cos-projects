from abc import ABC, abstractmethod
import random
from weather_report import WeatherReport

class WeatherSource(ABC):
    # Abstraction: We define the contract for fetching weather without 
    # specifying how it's done. Any source must implement this method.
    @abstractmethod
    def fetch_weather(self, city_name: str) -> WeatherReport:
        pass

class MockWeatherSource(WeatherSource):
    # Inheritance: MockWeatherSource inherits from the abstract WeatherSource 
    # and provides a concrete implementation using mock data.
    def __init__(self) -> None:
        self.known_cities = {
            "lagos": WeatherReport("Lagos", 32, "Sunny", 70, 15),
            "london": WeatherReport("London", 15, "Rainy", 85, 20),
            "new york": WeatherReport("New York", 22, "Cloudy", 60, 10),
            "tokyo": WeatherReport("Tokyo", 28, "Clear", 65, 12),
            "paris": WeatherReport("Paris", 18, "Partly Cloudy", 55, 8),
            "berlin": WeatherReport("Berlin", 12, "Cloudy", 65, 14),
            "sydney": WeatherReport("Sydney", 25, "Sunny", 50, 18),
            "dubai": WeatherReport("Dubai", 40, "Sunny", 40, 5),
        }
        self.conditions = ["Sunny", "Cloudy", "Rainy", "Stormy", "Clear", "Snowy"]

    def fetch_weather(self, city_name: str) -> WeatherReport:
        city_lower = city_name.strip().lower()
        if city_lower in self.known_cities:
            return self.known_cities[city_lower]
        
        # Fallback for unknown cities: randomly generate realistic data
        return WeatherReport(
            city=city_name.strip().title(),
            temperature=random.randint(-5, 40),
            condition=random.choice(self.conditions),
            humidity=random.randint(30, 90),
            wind_speed=random.randint(0, 30)
        )
