import json
import os
# pyrefly: ignore [missing-import]
import customtkinter as ctk
from typing import Optional
from weather_service import WeatherSource
from weather_report import WeatherReport

# UI Constants
BG_COLOR = "#FFFFFF"
TEXT_COLOR = "#1F2937"
ACCENT_COLOR = "#3B82F6"
BORDER_COLOR = "#E5E7EB"
FONT_FAMILY = "Helvetica"

class WeatherApp:
    # Encapsulation: We hide the application's internal state (_last_report, 
    # _weather_source) and expose only necessary methods to the outside.
    def __init__(self, root: ctk.CTk, weather_source: WeatherSource) -> None:
        self.root = root
        # Polymorphism: We depend on the abstract WeatherSource, not a concrete 
        # class. We can swap in a real API source without touching UI code.
        self._weather_source: WeatherSource = weather_source
        self._last_report: Optional[WeatherReport] = None
        self._settings_file = "settings.json"
        
        self._setup_ui()
        self._load_last_city()

    def _setup_ui(self) -> None:
        ctk.set_appearance_mode("Light")
        self.root.title("Weather Dashboard")
        self.root.geometry("400x550")
        self.root.configure(fg_color=BG_COLOR)
        
        self._setup_search_bar()
        self._setup_weather_card()

    def _setup_search_bar(self) -> None:
        self.search_frame = ctk.CTkFrame(self.root, fg_color=BG_COLOR)
        self.search_frame.pack(pady=20, padx=20, fill="x")
        
        self.city_entry = ctk.CTkEntry(
            self.search_frame, font=(FONT_FAMILY, 14), 
            placeholder_text="Enter city name...", text_color=TEXT_COLOR
        )
        self.city_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.city_entry.bind("<Return>", lambda e: self.search_city())
        
        self.search_btn = ctk.CTkButton(
            self.search_frame, text="Search", font=(FONT_FAMILY, 14, "bold"),
            fg_color=ACCENT_COLOR, text_color=BG_COLOR, command=self.search_city,
            width=80
        )
        self.search_btn.pack(side="right")
        
        self.status_label = ctk.CTkLabel(
            self.root, text="", font=(FONT_FAMILY, 12), text_color=TEXT_COLOR
        )
        self.status_label.pack(pady=5)

    def _setup_weather_card(self) -> None:
        self.card_frame = ctk.CTkFrame(
            self.root, fg_color=BG_COLOR, border_width=1, border_color=BORDER_COLOR,
            corner_radius=10
        )
        self.card_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        self.city_label = ctk.CTkLabel(
            self.card_frame, text="", font=(FONT_FAMILY, 24, "bold"), text_color=TEXT_COLOR
        )
        self.city_label.pack(pady=(20, 5))
        
        self.icon_label = ctk.CTkLabel(self.card_frame, text="", font=(FONT_FAMILY, 48))
        self.icon_label.pack(pady=0)
        
        self.temp_label = ctk.CTkLabel(
            self.card_frame, text="", font=(FONT_FAMILY, 64, "bold"), text_color=TEXT_COLOR
        )
        self.temp_label.pack(pady=0)
        
        self.condition_label = ctk.CTkLabel(
            self.card_frame, text="", font=(FONT_FAMILY, 18), text_color=TEXT_COLOR
        )
        self.condition_label.pack(pady=5)
        
        self.details_label = ctk.CTkLabel(
            self.card_frame, text="", font=(FONT_FAMILY, 14), text_color="#6B7280"
        )
        self.details_label.pack(pady=(15, 20))

    def search_city(self) -> None:
        city_name = self.city_entry.get().strip()
        if not city_name:
            self.status_label.configure(text="Please enter a city name")
            return
            
        self.status_label.configure(text="Loading...")
        self._clear_card()
        # Simulate network delay to keep UI responsive
        self.root.after(400, lambda: self._process_search(city_name))

    def _process_search(self, city_name: str) -> None:
        # Polymorphic call: _weather_source could be a mock or real API
        report = self._weather_source.fetch_weather(city_name)
        self._last_report = report
        self._save_last_city(city_name)
        
        self.status_label.configure(text="")
        self._update_display(report)

    def get_last_report(self) -> Optional[WeatherReport]:
        return self._last_report

    def _update_display(self, report: WeatherReport) -> None:
        icon = self._get_icon(report.condition)
        self.city_label.configure(text=report.city)
        self.icon_label.configure(text=icon)
        self.temp_label.configure(text=f"{report.temperature}°C")
        self.condition_label.configure(text=report.condition)
        self.details_label.configure(
            text=f"Humidity: {report.humidity}% | Wind: {report.wind_speed} km/h"
        )

    def _clear_card(self) -> None:
        self.city_label.configure(text="")
        self.icon_label.configure(text="")
        self.temp_label.configure(text="")
        self.condition_label.configure(text="")
        self.details_label.configure(text="")

    def _get_icon(self, condition: str) -> str:
        c = condition.lower()
        if "sunny" in c or "clear" in c: return "☀️"
        if "rain" in c or "storm" in c: return "🌧️"
        if "cloud" in c: return "☁️"
        if "snow" in c: return "❄️"
        return "🌤️"

    def _save_last_city(self, city_name: str) -> None:
        try:
            with open(self._settings_file, "w") as f:
                json.dump({"last_city": city_name}, f)
        except IOError:
            pass

    def _load_last_city(self) -> None:
        try:
            if os.path.exists(self._settings_file):
                with open(self._settings_file, "r") as f:
                    data = json.load(f)
                    if city := data.get("last_city", ""):
                        self.city_entry.insert(0, city)
                        self.search_city()
        except (IOError, json.JSONDecodeError):
            pass
