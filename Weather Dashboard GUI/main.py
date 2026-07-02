# pyrefly: ignore [missing-import]
import customtkinter as ctk
from weather_service import MockWeatherSource
from ui import WeatherApp

def main() -> None:
    root = ctk.CTk()
    
    # We instantiate the concrete MockWeatherSource here.
    # The UI only knows it as a WeatherSource.
    weather_source = MockWeatherSource()
    
    # Inject dependency into our app controller
    app = WeatherApp(root, weather_source)
    
    root.mainloop()

if __name__ == "__main__":
    main()
