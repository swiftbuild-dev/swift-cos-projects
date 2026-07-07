# pyrefly: ignore [missing-import]
import customtkinter as ctk
from stopwatch import Stopwatch

class StopwatchUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.stopwatch = Stopwatch()
        
        self.title("Stopwatch OOP Demo")
        self.geometry("400x600")
        self.configure(fg_color="#FFFFFF")
        
        # Center card frame, fixed size, prevents stretching when maximizing window
        self.card_frame = ctk.CTkFrame(
            self, width=340, height=520, fg_color="#FFFFFF",
            corner_radius=15, border_width=1, border_color="#E0E0E0"
        )
        self.card_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.card_frame.pack_propagate(False)

        # Time Display (Monospaced font to prevent jumping digits)
        self.time_label = ctk.CTkLabel(
            self.card_frame, text="00:00.0",
            font=ctk.CTkFont(family="Courier", size=54, weight="bold"),
            text_color="#1A1A1A"
        )
        self.time_label.pack(pady=(40, 20))

        # Main Control (Start/Stop)
        self.start_stop_btn = ctk.CTkButton(
            self.card_frame, text="Start",
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#007BFF", hover_color="#0056B3", text_color="#FFFFFF",
            width=160, height=45, corner_radius=8,
            command=self.handle_start_stop
        )
        self.start_stop_btn.pack(pady=10)

        # Secondary Controls Frame (Lap & Reset)
        self.secondary_frame = ctk.CTkFrame(self.card_frame, fg_color="transparent")
        self.secondary_frame.pack(pady=10)

        self.lap_btn = ctk.CTkButton(
            self.secondary_frame, text="Lap",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="transparent", hover_color="#F0F0F0",
            text_color="#007BFF", text_color_disabled="#A0A0A0",
            border_width=2, border_color="#007BFF",
            width=100, height=35, corner_radius=8,
            command=self.handle_lap, state="disabled"
        )
        self.lap_btn.grid(row=0, column=0, padx=10)

        self.reset_btn = ctk.CTkButton(
            self.secondary_frame, text="Reset",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="transparent", hover_color="#F0F0F0",
            text_color="#007BFF", text_color_disabled="#A0A0A0",
            border_width=2, border_color="#007BFF",
            width=100, height=35, corner_radius=8,
            command=self.handle_reset, state="disabled"
        )
        self.reset_btn.grid(row=0, column=1, padx=10)

        # Laps List Area (Scrollable)
        self.laps_frame = ctk.CTkScrollableFrame(
            self.card_frame, fg_color="transparent", 
            width=280, height=200
        )
        self.laps_frame.pack(pady=(20, 10), fill="both", expand=True)
        
        self.update_ui_state()

    def format_time(self, seconds: float) -> str:
        mins, secs = divmod(seconds, 60)
        return f"{int(mins):02d}:{secs:04.1f}"

    def update_display(self):
        current_time = self.stopwatch.get_elapsed_time()
        self.time_label.configure(text=self.format_time(current_time))
        
        if self.stopwatch.is_running():
            self.after(100, self.update_display)

    def handle_start_stop(self):
        self.stopwatch.start_stop()
        self.update_ui_state()
        
        if self.stopwatch.is_running():
            self.update_display()

    def handle_reset(self):
        self.stopwatch.reset()
        self.time_label.configure(text="00:00.0")
        self.update_ui_state()
        self.refresh_laps_list()

    def handle_lap(self):
        self.stopwatch.record_lap()
        self.refresh_laps_list()

    def refresh_laps_list(self):
        # Clear existing lap rows
        for widget in self.laps_frame.winfo_children():
            widget.destroy()
            
        laps = self.stopwatch.get_laps()
        lap_count = len(laps)
        
        for i, lap_time in enumerate(laps):
            row = ctk.CTkFrame(self.laps_frame, fg_color="transparent")
            row.pack(fill="x", pady=4)
            
            num_lbl = ctk.CTkLabel(
                row, text=f"Lap {lap_count - i}", 
                text_color="#666666", font=ctk.CTkFont(size=14)
            )
            num_lbl.pack(side="left", padx=10)
            
            time_lbl = ctk.CTkLabel(
                row, text=self.format_time(lap_time),
                text_color="#1A1A1A", font=ctk.CTkFont(family="Courier", size=14, weight="bold")
            )
            time_lbl.pack(side="right", padx=10)
            
            # Draw divider line between laps
            if i < len(laps) - 1:
                divider = ctk.CTkFrame(self.laps_frame, height=1, fg_color="#F0F0F0")
                divider.pack(fill="x", padx=10, pady=2)

    def update_ui_state(self):
        if self.stopwatch.is_running():
            self.start_stop_btn.configure(
                text="Stop", fg_color="#DC3545", hover_color="#C82333"
            )
            self.lap_btn.configure(state="normal")
            self.reset_btn.configure(state="disabled")
        else:
            self.start_stop_btn.configure(
                text="Start", fg_color="#007BFF", hover_color="#0056B3"
            )
            self.lap_btn.configure(state="disabled")
            
            if self.stopwatch.is_idle():
                self.reset_btn.configure(state="disabled")
            else:
                self.reset_btn.configure(state="normal")
