import tkinter as tk
from tkinter import messagebox
from gui.students_page import StudentsPage
from gui.teachers_page import TeachersPage
from gui.uniforms_page import UniformsPage
from gui.stationery_page import StationeryPage
from gui.fee_page import FeePage
from gui.receipts_page import ReceiptsPage
from gui.attendance_page import AttendancePage
from gui.attendance_salary_page import AttendanceSalaryPage
from gui.todo_page import TodoPage
from database import init_db, get_connection
from datetime import datetime, timedelta

# Initialize database tables
init_db()

class RoundedButton(tk.Canvas):
    def __init__(self, parent, text, command=None, width=280, height=60,
                 bg="#3498db", fg="white", hover_bg="#2980b9", radius=25, font=("Arial", 14, "bold")):
        super().__init__(parent, width=width, height=height, highlightthickness=0, bg=parent["bg"])
        self.command = command
        self.bg = bg
        self.hover_bg = hover_bg
        self.radius = radius
        self.font = font
        self.fg = fg
        self.text = text

        # Draw rounded rectangle
        self.rect = self.create_rounded_rect(0, 0, width, height, radius, fill=bg, outline=bg)
        self.label = self.create_text(width//2, height//2, text=text, fill=fg, font=font)
        self.bind_events()

    def create_rounded_rect(self, x1, y1, x2, y2, r=25, **kwargs):
        points = [x1+r, y1,
                  x1+r, y1,
                  x2-r, y1,
                  x2-r, y1,
                  x2, y1,
                  x2, y1+r,
                  x2, y1+r,
                  x2, y2-r,
                  x2, y2-r,
                  x2, y2,
                  x2-r, y2,
                  x2-r, y2,
                  x1+r, y2,
                  x1+r, y2,
                  x1, y2,
                  x1, y2-r,
                  x1, y2-r,
                  x1, y1+r,
                  x1, y1+r,
                  x1, y1]
        return self.create_polygon(points, smooth=True, **kwargs)

    def bind_events(self):
        self.tag_bind(self.rect, "<Button-1>", lambda e: self.command() if self.command else None)
        self.tag_bind(self.label, "<Button-1>", lambda e: self.command() if self.command else None)
        self.tag_bind(self.rect, "<Enter>", lambda e: self.itemconfig(self.rect, fill=self.hover_bg))
        self.tag_bind(self.label, "<Enter>", lambda e: self.itemconfig(self.rect, fill=self.hover_bg))
        self.tag_bind(self.rect, "<Leave>", lambda e: self.itemconfig(self.rect, fill=self.bg))
        self.tag_bind(self.label, "<Leave>", lambda e: self.itemconfig(self.rect, fill=self.bg))

class MainApp:
    def __init__(self):
        self.win = tk.Tk()
        self.win.title("School Management System")
        self.win.geometry("1000x800")
        self.win.configure(bg="#f0f0f0")

        # ---------------- Header ----------------
        tk.Label(self.win, text="School Management System",
                 font=("Arial", 20, "bold"),
                 bg="#2c3e50", fg="white", pady=20).pack(fill="x")

        # ---------------- Button Frame ----------------
        frame = tk.Frame(self.win, bg="#f0f0f0")
        frame.pack(pady=50)

        # ---------------- Helper Function ----------------
        def add_button(text, PageClass, row, col):
            btn = RoundedButton(frame, text=text, command=PageClass)
            btn.grid(row=row, column=col, padx=25, pady=25)
            return btn

        # ---------------- Module Buttons ----------------
        add_button("Student Management", StudentsPage, 0, 0)
        add_button("Teacher Management", TeachersPage, 0, 1)
        add_button("Uniform Inventory", UniformsPage, 1, 0)
        add_button("Stationery Inventory", StationeryPage, 1, 1)
        add_button("Fees Module", FeePage, 2, 0)
        add_button("Receipts Manager", ReceiptsPage, 2, 1)
        add_button("Teacher Attendance", AttendancePage, 3, 0)
        add_button("Attendance/Salary Chart", AttendanceSalaryPage, 3, 1)
        add_button("To-Do List", TodoPage, 4, 0)

        # ---------------- Remove Old Records Button ----------------
        def remove_old_records():
            confirm = messagebox.askyesno("Confirm Deletion",
                                          "Are you sure you want to delete records older than 3 months?")
            if not confirm:
                return

            three_months_ago = datetime.now() - timedelta(days=90)
            cutoff = three_months_ago.strftime("%Y-%m-%d")
            conn = get_connection()
            cur = conn.cursor()
            try:
                cur.execute("DELETE FROM fees WHERE date_issued < ?", (cutoff,))
                cur.execute("DELETE FROM receipts WHERE date_issued < ?", (cutoff,))
                cur.execute("DELETE FROM teacher_attendance WHERE date < ?", (cutoff,))
                conn.commit()
                messagebox.showinfo("Success", f"Records prior to {cutoff} deleted successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to remove old records:\n{str(e)}")
            finally:
                conn.close()

        delete_btn = RoundedButton(frame, "Remove Records > 3 Months", command=remove_old_records,
                                   bg="#e74c3c", hover_bg="#c0392b", width=350, height=70)
        delete_btn.grid(row=4, column=1, padx=25, pady=25)

        self.win.mainloop()


if __name__ == "__main__":
    MainApp()

