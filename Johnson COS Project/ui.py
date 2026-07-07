# pyrefly: ignore [missing-import]
import customtkinter as ctk
from datetime import datetime
from main import WeekdayAlarm, WeekendAlarm, Alarm

class AlarmClockApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        self.title("Basic Alarm Clock")
        self.geometry("400x450")
        self.configure(fg_color="#FFFFFF")
        
        self.active_alarm: Alarm | None = None
        self.is_ringing: bool = False
        self.accent_color: str = "#3B82F6"
        self.base_font: str = "Helvetica"
        self.text_color: str = "#1F2937"

        self._create_widgets()
        self._update_clock()

    def _create_widgets(self) -> None:
        # Fixed-width content frame centered in the window
        self.content_frame = ctk.CTkFrame(
            self, 
            width=340, 
            height=400,
            fg_color="#FFFFFF",
            border_width=1,
            border_color="#E5E7EB",
            corner_radius=12
        )
        self.content_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.content_frame.pack_propagate(False)

        # Padding container
        self.inner_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.inner_frame.pack(fill="both", expand=True, padx=16, pady=16)

        # Clock Display
        self.time_label = ctk.CTkLabel(
            self.inner_frame, 
            text="00:00:00",
            font=ctk.CTkFont(family="Courier", size=48, weight="bold"),
            text_color=self.text_color
        )
        self.time_label.pack(pady=(20, 10))

        self.alert_label = ctk.CTkLabel(
            self.inner_frame,
            text="",
            font=ctk.CTkFont(family=self.base_font, size=14, weight="bold"),
            text_color=self.accent_color
        )
        self.alert_label.pack(pady=(0, 15))

        # Alarm Type Dropdown
        self.alarm_type_var = ctk.StringVar(value="Weekday Alarm")
        self.type_dropdown = ctk.CTkOptionMenu(
            self.inner_frame,
            values=["Weekday Alarm", "Weekend Alarm"],
            variable=self.alarm_type_var,
            fg_color="#FFFFFF",
            button_color="#F3F4F6",
            button_hover_color="#E5E7EB",
            text_color=self.text_color,
            font=ctk.CTkFont(family=self.base_font, size=14)
        )
        self.type_dropdown.pack(fill="x", pady=12)

        # Time Inputs
        self.time_input_frame = ctk.CTkFrame(self.inner_frame, fg_color="transparent")
        self.time_input_frame.pack(pady=12)

        self.hour_var = ctk.StringVar(value="08")
        self.hour_dropdown = ctk.CTkOptionMenu(
            self.time_input_frame,
            values=[f"{i:02d}" for i in range(24)],
            variable=self.hour_var,
            width=80,
            fg_color="#FFFFFF",
            button_color="#F3F4F6",
            button_hover_color="#E5E7EB",
            text_color=self.text_color,
            font=ctk.CTkFont(family=self.base_font, size=14)
        )
        self.hour_dropdown.pack(side="left", padx=5)

        colon_label = ctk.CTkLabel(
            self.time_input_frame, 
            text=":", 
            font=ctk.CTkFont(family=self.base_font, size=20, weight="bold"),
            text_color=self.text_color
        )
        colon_label.pack(side="left")

        self.minute_var = ctk.StringVar(value="00")
        self.minute_dropdown = ctk.CTkOptionMenu(
            self.time_input_frame,
            values=[f"{i:02d}" for i in range(60)],
            variable=self.minute_var,
            width=80,
            fg_color="#FFFFFF",
            button_color="#F3F4F6",
            button_hover_color="#E5E7EB",
            text_color=self.text_color,
            font=ctk.CTkFont(family=self.base_font, size=14)
        )
        self.minute_dropdown.pack(side="left", padx=5)

        # Buttons
        self.set_button = ctk.CTkButton(
            self.inner_frame,
            text="Set Alarm",
            command=self._set_alarm,
            fg_color=self.accent_color,
            text_color="#FFFFFF",
            hover_color="#2563EB",
            font=ctk.CTkFont(family=self.base_font, size=14, weight="bold"),
            height=40
        )
        self.set_button.pack(fill="x", pady=12)

        self.stop_button = ctk.CTkButton(
            self.inner_frame,
            text="Stop Alarm",
            command=self._stop_alarm,
            fg_color="#FFFFFF",
            text_color=self.accent_color,
            border_width=2,
            border_color=self.accent_color,
            hover_color="#EFF6FF",
            font=ctk.CTkFont(family=self.base_font, size=14, weight="bold"),
            height=40
        )
        # Hidden initially

    def _set_alarm(self) -> None:
        alarm_type = self.alarm_type_var.get()
        
        if alarm_type == "Weekday Alarm":
            self.active_alarm = WeekdayAlarm()
        else:
            self.active_alarm = WeekendAlarm()
            
        hour = int(self.hour_var.get())
        minute = int(self.minute_var.get())
        
        self.active_alarm.set_time(hour, minute)
        self.alert_label.configure(text=f"Alarm set for {hour:02d}:{minute:02d}")
        self._reset_ui_state()

    def _stop_alarm(self) -> None:
        self.alert_label.configure(text="")
        self._reset_ui_state()

    def _reset_ui_state(self) -> None:
        self.is_ringing = False
        self.time_label.configure(text_color=self.text_color)
        self.stop_button.pack_forget()

    def _update_clock(self) -> None:
        now = datetime.now()
        self.time_label.configure(text=now.strftime("%H:%M:%S"))

        # Polymorphism: The app doesn't need to check which alarm type is active,
        # it just calls .check() and the correct method is executed.
        if self.active_alarm and not self.is_ringing:
            if self.active_alarm.check(now) and now.second == 0:
                self.is_ringing = True
                self.time_label.configure(text_color=self.accent_color)
                self.alert_label.configure(text="⏰ Alarm!")
                self.stop_button.pack(fill="x", pady=12)

        self.after(1000, self._update_clock)
