import tkinter as tk
from database import get_connection
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class AttendanceSalaryPage:
    def __init__(self):
        self.win = tk.Toplevel()
        self.win.title("Teacher Attendance & Salary")
        self.win.geometry("900x600")
        self.win.configure(bg="#f0f0f0")

        tk.Label(self.win, text="Teacher Attendance & Salary (Last Month)",
                 font=("Arial", 16, "bold"), bg="#2c3e50", fg="white", pady=10).pack(fill="x")

        self.load_chart()

    def load_chart(self):
        conn = get_connection()
        cur = conn.cursor()
        last_month = datetime.now() - timedelta(days=30)
        cutoff = last_month.strftime("%Y-%m-%d")

        cur.execute("""
            SELECT teacher_name, COUNT(*) as present_days
            FROM teacher_attendance
            WHERE date >= ?
            GROUP BY teacher_name
        """, (cutoff,))
        data = cur.fetchall()
        conn.close()

        if not data:
            tk.Label(self.win, text="No attendance data for last month.", font=("Arial", 14)).pack(pady=20)
            return

        names = [d[0] for d in data]
        days = [d[1] for d in data]
        salary_per_day = 1000  # example
        salaries = [d*salary_per_day for d in days]

        fig, ax = plt.subplots(figsize=(8,5))
        ax.bar(names, days, color="#3498db")
        ax.set_ylabel("Days Present")
        ax.set_title("Last Month Teacher Attendance")
        for i, s in enumerate(salaries):
            ax.text(i, days[i]+0.2, f"₹{s}", ha='center', fontweight='bold')
        plt.xticks(rotation=30)
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.win)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=20)
