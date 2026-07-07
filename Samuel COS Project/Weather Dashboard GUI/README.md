# Weather Dashboard GUI

A beautiful weather monitoring application. It simulates fetching weather data from external sources and displays temperature, humidity, wind speed, and weather conditions for different cities.

## Key Components

### 1. The Weather Source Contract
Defines how the app expects to receive weather data.
```python
class WeatherSource(ABC):
    @abstractmethod
    def fetch_weather(self, city_name: str) -> WeatherReport:
        pass
```

### 2. The Mock Implementation
```python
class MockWeatherSource(WeatherSource):
    def fetch_weather(self, city_name: str) -> WeatherReport:
        # Fallback for unknown cities: randomly generate realistic data
        return WeatherReport(
            city=city_name.strip().title(),
            temperature=random.randint(-5, 40),
            condition=random.choice(self.conditions),
            # ...
        )
```

## The Four Pillars of OOP in this Project

This project is a perfect example of Object-Oriented Programming (OOP). Here's how the four main pillars are used:

1. **Abstraction**: 
   - **Where it is**: The `WeatherSource` base class (`weather_service.py`).
   - **How it works**: It provides a clean contract: "Give me a city name, and I will return a `WeatherReport`." The rest of the app doesn't know (or care) if the data comes from a real internet API or a fake mock generator. The complicated details are abstracted away.

2. **Inheritance**: 
   - **Where it is**: The `MockWeatherSource` class (`weather_service.py`).
   - **How it works**: It inherits the interface from `WeatherSource` and then actually provides the concrete implementation for how to build fake weather data. 

3. **Encapsulation**: 
   - **Where it is**: The `WeatherReport` data class (`weather_report.py`).
   - **How it works**: Instead of passing around 5 different variables (temperature, city name, wind speed, etc.) to every part of the user interface, we bundle them all securely inside a single `WeatherReport` object.

4. **Polymorphism**: 
   - **Where it is**: Calling `fetch_weather()` in the UI code.
   - **How it works**: The UI can be given *any* object that is a `WeatherSource`. Right now it's a `MockWeatherSource`, but in the future, if you build an `InternetWeatherSource`, the UI code won't need to change at all! It will just call `.fetch_weather()` and polymorphically get the right data.
