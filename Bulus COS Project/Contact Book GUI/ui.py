# pyrefly: ignore [missing-import]
import customtkinter as ctk
import tkinter.messagebox as messagebox
from main import ContactBook, PersonalContact, WorkContact

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Contact Book")
        self.geometry("420x600")
        self.configure(fg_color="#FFFFFF")
        
        self.book = ContactBook()
        self.accent_color = "#3B82F6"
        
        self._setup_ui()
        self.refresh_list()

    def _setup_ui(self):
        self.card = ctk.CTkFrame(self, width=380, fg_color="#FFFFFF", border_width=1, border_color="#E5E7EB", corner_radius=12)
        self.card.place(relx=0.5, rely=0.5, anchor="center")
        
        lbl_title = ctk.CTkLabel(self.card, text="Add Contact", font=("Arial", 20, "bold"), text_color="#1F2937")
        lbl_title.pack(pady=(20, 10), padx=20, anchor="w")
        
        self.type_var = ctk.StringVar(value="Personal")
        self.type_menu = ctk.CTkOptionMenu(self.card, variable=self.type_var, values=["Personal", "Work"], 
                                           command=self.on_type_change, fg_color="#FFFFFF", text_color="#1F2937", 
                                           button_color="#E5E7EB", button_hover_color="#D1D5DB", font=("Arial", 14))
        self.type_menu.pack(pady=(0, 10), padx=20, fill="x")
        
        self.entry_name = ctk.CTkEntry(self.card, placeholder_text="Name", fg_color="#FFFFFF", border_color="#E5E7EB", text_color="#1F2937", font=("Arial", 14))
        self.entry_name.pack(pady=5, padx=20, fill="x")
        
        self.entry_phone = ctk.CTkEntry(self.card, placeholder_text="Phone Number", fg_color="#FFFFFF", border_color="#E5E7EB", text_color="#1F2937", font=("Arial", 14))
        self.entry_phone.pack(pady=5, padx=20, fill="x")
        
        self.entry_specific = ctk.CTkEntry(self.card, placeholder_text="Relationship", fg_color="#FFFFFF", border_color="#E5E7EB", text_color="#1F2937", font=("Arial", 14))
        self.entry_specific.pack(pady=5, padx=20, fill="x")
        
        btn_add = ctk.CTkButton(self.card, text="Save Contact", fg_color=self.accent_color, hover_color="#2563EB", text_color="#FFFFFF", font=("Arial", 14, "bold"), command=self.add_contact)
        btn_add.pack(pady=(10, 20), padx=20, fill="x")
        
        divider = ctk.CTkFrame(self.card, height=1, fg_color="#E5E7EB")
        divider.pack(fill="x", padx=20, pady=5)
        
        lbl_list = ctk.CTkLabel(self.card, text="Contacts", font=("Arial", 20, "bold"), text_color="#1F2937")
        lbl_list.pack(pady=(10, 5), padx=20, anchor="w")
        
        self.entry_search = ctk.CTkEntry(self.card, placeholder_text="Search by name...", fg_color="#FFFFFF", border_color="#E5E7EB", text_color="#1F2937", font=("Arial", 14))
        self.entry_search.pack(pady=5, padx=20, fill="x")
        self.entry_search.bind("<KeyRelease>", self.refresh_list)
        
        self.list_frame = ctk.CTkScrollableFrame(self.card, fg_color="#FFFFFF", height=200)
        self.list_frame.pack(pady=(10, 20), padx=20, fill="x")

    def on_type_change(self, choice: str):
        placeholder = "Relationship" if choice == "Personal" else "Company"
        self.entry_specific.configure(placeholder_text=placeholder)

    def add_contact(self):
        name, phone, specific = self.entry_name.get().strip(), self.entry_phone.get().strip(), self.entry_specific.get().strip()
        
        if not name or not phone or not specific:
            return messagebox.showerror("Error", "All fields are required")
            
        contact = PersonalContact(name, phone, specific) if self.type_var.get() == "Personal" else WorkContact(name, phone, specific)
        self.book.add_contact(contact)
        
        self.entry_name.delete(0, 'end')
        self.entry_phone.delete(0, 'end')
        self.entry_specific.delete(0, 'end')
        self.refresh_list()

    def delete_contact(self, name: str):
        if messagebox.askyesno("Confirm", f"Delete {name}?"):
            self.book.remove_contact(name)
            self.refresh_list()

    def refresh_list(self, event=None):
        for widget in self.list_frame.winfo_children():
            widget.destroy()
            
        query = self.entry_search.get().strip()
        contacts = self.book.search_contacts(query) if query else self.book.get_all_contacts()
        
        for contact in contacts:
            row = ctk.CTkFrame(self.list_frame, fg_color="#FFFFFF")
            row.pack(fill="x", pady=2)
            
            # Polymorphism: The book doesn't know if contact is Personal or Work,
            # it just calls display_details() and gets the right format back.
            details = contact.display_details()
            parts = details.split(" — ")
            name_text, sub_text = parts[0], " — ".join(parts[1:])
            
            info_frame = ctk.CTkFrame(row, fg_color="#FFFFFF")
            info_frame.pack(side="left", fill="x", expand=True)
            
            ctk.CTkLabel(info_frame, text=name_text, font=("Arial", 14, "bold"), text_color="#374151").pack(anchor="w")
            ctk.CTkLabel(info_frame, text=sub_text, font=("Arial", 12), text_color="#9CA3AF").pack(anchor="w")
            
            btn_del = ctk.CTkButton(row, text="Del", width=40, fg_color="#FFFFFF", border_color=self.accent_color, 
                                    border_width=1, text_color=self.accent_color, hover_color="#F3F4F6", font=("Arial", 12, "bold"),
                                    command=lambda n=contact.name: self.delete_contact(n))
            btn_del.pack(side="right", padx=5)
            
            ctk.CTkFrame(self.list_frame, height=1, fg_color="#F3F4F6").pack(fill="x", pady=2)

if __name__ == "__main__":
    app = App()
    app.mainloop()
