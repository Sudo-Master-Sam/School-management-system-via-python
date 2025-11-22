import tkinter as tk
from gui.students_page import StudentsPage
from gui.teachers_page import TeachersPage
from gui.uniforms_page import UniformsPage
from gui.stationery_page import StationeryPage
from gui.fee_page import FeePage
from gui.receipts_page import ReceiptsPage
from gui.attendance_page import AttendancePage  # <-- import AttendancePage
from database import init_db

# Initialize database tables
init_db()

class MainApp:
    def __init__(self):
        self.win = tk.Tk()
        self.win.title("School Management System")
        self.win.geometry("800x600")
        self.win.configure(bg="#f0f0f0")

        # Header
        tk.Label(self.win, text="School Management System",
                 font=("Arial", 26, "bold"),
                 bg="#2c3e50", fg="white", pady=20).pack(fill="x")

        frame = tk.Frame(self.win, bg="#f0f0f0")
        frame.pack(pady=50)

        btn_color = "#3498db"
        btn_hover = "#2980b9"

        # Helper to create buttons
        def create_button(text, PageClass, row, col):
            def open_page():
                PageClass()  # Opens the respective page when clicked
            b = tk.Button(frame, text=text, width=20, height=2, bg=btn_color, fg="white", command=open_page)
            b.grid(row=row, column=col, padx=20, pady=20)
            b.bind("<Enter>", lambda e: b.config(bg=btn_hover))
            b.bind("<Leave>", lambda e: b.config(bg=btn_color))

        # Buttons
        create_button("Student Management", StudentsPage, 0, 0)
        create_button("Teacher Management", TeachersPage, 0, 1)
        create_button("Uniform Inventory", UniformsPage, 1, 0)
        create_button("Stationery Inventory", StationeryPage, 1, 1)
        create_button("Fees Module", FeePage, 2, 0)
        create_button("Receipts Manager", ReceiptsPage, 2, 1)
        create_button("Teacher Attendance", AttendancePage, 3, 0)  # <-- Added Attendance button

        self.win.mainloop()

if __name__ == "__main__":
    MainApp()
