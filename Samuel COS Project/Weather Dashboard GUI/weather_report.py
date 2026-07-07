from dataclasses import dataclass

@dataclass
class WeatherReport:
    # Encapsulation: Grouping related data fields into a single, cohesive 
    # object rather than passing around individual variables.
    city: str
    temperature: int
    condition: str
    humidity: int
    wind_speed: int
