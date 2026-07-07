# pyrefly: ignore [missing-import]
import customtkinter as ctk
from main import EventCountdown, StudyCountdown, Countdown

class TimerApp(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color="#FFFFFF")
        self.geometry("380x400")
        self.resizable(False, False)
        self.title("Timer")
        
        self.timer: Countdown | None = None
        self.is_paused = False
        self._timer_id = None
        font = ("Arial", 14)
        
        frame = ctk.CTkFrame(self, fg_color="#FFFFFF")
        frame.place(relx=0.5, rely=0.5, anchor="center")
        
        self.type_var = ctk.StringVar(value="Event")
        ctk.CTkOptionMenu(frame, variable=self.type_var, values=["Event", "Study"], font=font,
                          fg_color="#FFFFFF", text_color="#333333", button_color="#EEEEEE").pack(pady=14)
                          
        self.sec_entry = ctk.CTkEntry(frame, font=font, fg_color="#FFFFFF", 
                                      border_color="#CCCCCC", text_color="#333333")
        self.sec_entry.insert(0, "60")
        self.sec_entry.pack(pady=14)
        
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(pady=14)
        ctk.CTkButton(btn_frame, text="Start", font=font, fg_color="#007BFF", 
                      text_color="#FFFFFF", command=self.start, width=100).pack(side="left", padx=5)
        self.pause_button = ctk.CTkButton(btn_frame, text="Pause", font=font, fg_color="#6C757D", 
                                          text_color="#FFFFFF", command=self.toggle_pause, width=100)
        self.pause_button.pack(side="left", padx=5)
                      
        self.display = ctk.CTkLabel(frame, text="00", font=("Arial", 48, "bold"), text_color="#333333")
        self.display.pack(pady=14)
        
    def start(self):
        if self._timer_id is not None:
            self.after_cancel(self._timer_id)
        sec = int(self.sec_entry.get())
        self.timer = EventCountdown(sec) if self.type_var.get() == "Event" else StudyCountdown(sec)
        self.is_paused = False
        self.pause_button.configure(text="Pause")
        self.display.configure(text=str(sec))
        self._timer_id = self.after(1000, self.update_timer)
        
    def toggle_pause(self):
        if not self.timer or self.timer.is_done(): return
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.pause_button.configure(text="Resume")
            if self._timer_id is not None:
                self.after_cancel(self._timer_id)
                self._timer_id = None
        else:
            self.pause_button.configure(text="Pause")
            self._timer_id = self.after(1000, self.update_timer)
        
    def update_timer(self):
        if not self.timer or self.is_paused: return
        val = self.timer.tick()
        
        if self.timer.is_done():
            # Polymorphism: uniform call across different subclasses
            self.display.configure(text=self.timer.on_finish())
            self._timer_id = None
        else:
            self.display.configure(text=str(val))
            self._timer_id = self.after(1000, self.update_timer)

if __name__ == "__main__":
    TimerApp().mainloop()
