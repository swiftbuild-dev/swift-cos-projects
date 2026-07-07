# Weather Dashboard GUI

## 🚀 Core Functionality
A desktop weather dashboard where you type in a city name and get back current weather information including temperature, weather condition (e.g., Sunny, Rainy), humidity, and wind speed. It uses a mock data service that has real data for popular cities and generates realistic random data for unknown ones.

## 🧠 The Four Pillars of OOP (Object-Oriented Programming)

### 1. 🔒 Abstraction — *Hiding the complex details*
Abstraction is like a vending machine — you press a button for a drink without seeing the mechanism inside. `WeatherSource` defines *what* every data source must do (provide a `fetch_weather()` method), without saying *how* it gets the data. The UI never needs to worry about those details.

```python
# Every weather source MUST be able to fetch weather for a city.
# The blueprint hides HOW — only the subclass decides that.
class WeatherSource(ABC):
    @abstractmethod
    def fetch_weather(self, city_name: str) -> WeatherReport:
        pass
```

### 2. 👪 Inheritance — *Passing down traits*
Inheritance lets a new class build on an existing one. `MockWeatherSource` inherits from `WeatherSource`, getting its structure automatically. It then fills in the concrete `fetch_weather()` logic using a dictionary of known cities.

```python
# MockWeatherSource inherits the WeatherSource contract,
# and provides its own real implementation.
class MockWeatherSource(WeatherSource):
    def fetch_weather(self, city_name: str) -> WeatherReport:
        city_lower = city_name.strip().lower()
        if city_lower in self.known_cities:
            return self.known_cities[city_lower]
        # For unknown cities, generate random realistic data
        return WeatherReport(city=city_name.title(), ...)
```

### 3. 🔄 Polymorphism — *Many forms, one call*
Polymorphism means you can swap out the underlying data source without changing the UI. Today the app uses `MockWeatherSource`. Tomorrow it could use a `LiveAPIWeatherSource` — the UI would call `fetch_weather()` in exactly the same way and get a result regardless.

```python
# The UI stores whichever source is active and just calls fetch_weather().
# It doesn't care if it's mock data or a live API — same method, same result shape.
report = self.weather_source.fetch_weather(city_name)
```

### 4. 📦 Encapsulation — *Protecting the data*
Encapsulation bundles data and logic safely together. The `WeatherReport` object holds all its weather data fields together in one place, and `MockWeatherSource` keeps its dictionary of known cities bundled inside itself — preventing outside code from accidentally corrupting the source data.

```python
class MockWeatherSource(WeatherSource):
    def __init__(self) -> None:
        # All city data is safely bundled inside this class.
        self.known_cities = {
            "lagos": WeatherReport("Lagos", 32, "Sunny", 70, 15),
            "london": WeatherReport("London", 15, "Rainy", 85, 20),
            # ...more cities
        }
```
