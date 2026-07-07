# pyrefly: ignore [missing-import]
import customtkinter as ctk
from main import AttendanceTracker

class AttendanceApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.tracker = AttendanceTracker()

        self.title("Attendance Tracker")
        self.geometry("420x600")
        self.configure(fg_color="#FFFFFF") # Pure white background

        # One consistent font, 2 sizes only
        self.font_heading = ("Inter", 16, "bold")
        self.font_details = ("Inter", 12)

        # Content frame (fixed width, centered, white with thin light-gray border)
        self.main_frame = ctk.CTkFrame(
            self, 
            width=380, 
            height=540, 
            fg_color="#FFFFFF",
            border_width=1,
            border_color="#E5E7EB"
        )
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.main_frame.pack_propagate(False) # Don't shrink to fit contents

        # Header
        self.title_label = ctk.CTkLabel(
            self.main_frame, 
            text="Student Attendance", 
            font=self.font_heading, 
            text_color="#111827"
        )
        self.title_label.pack(pady=(20, 10))

        # Hardcoded starter list of students
        self.students = ["Alice Smith", "Bob Jones", "Charlie Brown", "Diana Prince"]
        
        self.student_var = ctk.StringVar(value=self.students[0])
        self.student_dropdown = ctk.CTkOptionMenu(
            self.main_frame,
            values=self.students,
            variable=self.student_var,
            font=self.font_details,
            fg_color="#F3F4F6",
            text_color="#111827",
            button_color="#E5E7EB",
            button_hover_color="#D1D5DB",
            dropdown_font=self.font_details,
            command=self.on_student_change
        )
        self.student_dropdown.pack(pady=12, padx=16, fill="x")

        # Buttons Frame
        self.btn_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.btn_frame.pack(pady=12, padx=16, fill="x")
        self.btn_frame.grid_columnconfigure((0, 1), weight=1)

        self.btn_present = ctk.CTkButton(
            self.btn_frame, 
            text="Mark Present",
            font=self.font_details,
            fg_color="#3B82F6", # Accent Blue
            text_color="#FFFFFF",
            hover_color="#2563EB",
            command=lambda: self.mark("present")
        )
        self.btn_present.grid(row=0, column=0, padx=(0, 6), sticky="ew")

        self.btn_absent = ctk.CTkButton(
            self.btn_frame, 
            text="Mark Absent",
            font=self.font_details,
            fg_color="#FFFFFF",
            text_color="#EF4444", # Muted Red text
            border_width=1,
            border_color="#EF4444", # Muted Red outline
            hover_color="#FEF2F2",
            command=lambda: self.mark("absent")
        )
        self.btn_absent.grid(row=0, column=1, padx=(6, 0), sticky="ew")

        # Stats Label (attendance rate)
        self.stats_label = ctk.CTkLabel(
            self.main_frame, 
            text="", 
            font=self.font_heading, 
            text_color="#374151" # Dark gray
        )
        self.stats_label.pack(pady=(16, 8))

        # Divider
        self.divider = ctk.CTkFrame(self.main_frame, height=1, fg_color="#E5E7EB")
        self.divider.pack(fill="x", padx=16, pady=8)

        # Records List
        self.records_frame = ctk.CTkScrollableFrame(
            self.main_frame, 
            fg_color="transparent",
            scrollbar_button_color="#E5E7EB",
            scrollbar_button_hover_color="#D1D5DB"
        )
        self.records_frame.pack(fill="both", expand=True, padx=16, pady=(8, 16))

        # Initial UI refresh
        self.update_ui()

    def on_student_change(self, choice):
        self.update_ui()

    def mark(self, status: str):
        student = self.student_var.get()
        self.tracker.mark_attendance(student, status)
        self.update_ui()

    def update_ui(self):
        student = self.student_var.get()
        
        # Update stats
        rate = self.tracker.get_attendance_rate(student)
        self.stats_label.configure(text=f"{student}: {rate:.0f}% present")

        # Clear records frame
        for widget in self.records_frame.winfo_children():
            widget.destroy()

        # Update records list
        records = self.tracker.get_all_records()
        for record in records:
            row = ctk.CTkFrame(self.records_frame, fg_color="transparent")
            row.pack(fill="x", pady=6, padx=4)

            name_date = f"{record.student_name} • {record.date_str}"
            label_name = ctk.CTkLabel(row, text=name_date, font=self.font_details, text_color="#6B7280")
            label_name.pack(side="left")

            # Polymorphism: Calling status_label() without knowing if it's PresentRecord or AbsentRecord.
            # The tracker and UI don't care about the exact subclass type, they just trust the method exists.
            status_text = record.status_label()
            color = "#10B981" if "Present" in status_text else "#EF4444" # Soft green or Soft red
            
            label_status = ctk.CTkLabel(row, text=status_text, font=self.font_details, text_color=color)
            label_status.pack(side="right")

            # Thin divider between rows
            row_divider = ctk.CTkFrame(self.records_frame, height=1, fg_color="#F3F4F6")
            row_divider.pack(fill="x", padx=4)

if __name__ == "__main__":
    app = AttendanceApp()
    app.mainloop()
