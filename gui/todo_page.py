import tkinter as tk
from tkinter import simpledialog, messagebox
from database import get_connection

class TodoPage:
    def __init__(self):
        self.win = tk.Toplevel()
        self.win.title("To-Do List")
        self.win.geometry("800x650")
        self.win.configure(bg="#f0f0f0")

        # Header
        tk.Label(self.win, text="To-Do List", font=("Arial", 16, "bold"),
                 bg="#2c3e50", fg="white", pady=10).pack(fill="x")

        # Frame for tasks + scrollbar
        self.tasks_frame = tk.Frame(self.win, bg="#f0f0f0")
        self.tasks_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.listbox = tk.Listbox(self.tasks_frame, width=40, height=15, font=("Arial", 12))
        self.listbox.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(self.tasks_frame)
        scrollbar.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

        # Buttons frame
        btn_frame = tk.Frame(self.win, bg="#f0f0f0")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Add Task", width=12, command=self.add_task).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Toggle Done", width=12, command=self.toggle_done).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Delete Task", width=12, command=self.delete_task).grid(row=0, column=2, padx=5)

        # Load tasks initially
        self.load_tasks()

    # ---------------- DB Operations ----------------
    def load_tasks(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS todo (id INTEGER PRIMARY KEY, task TEXT, done INTEGER)")
        cur.execute("SELECT task, done FROM todo")
        self.listbox.delete(0, "end")
        for task, done in cur.fetchall():
            self.listbox.insert("end", f"[{'x' if done else ' '}] {task}")
        conn.close()

    def add_task(self):
        task_text = simpledialog.askstring("Add Task", "Enter task:")
        if task_text:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO todo (task, done) VALUES (?, 0)", (task_text,))
            conn.commit()
            conn.close()
            self.load_tasks()

    def toggle_done(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showwarning("Select Task", "Please select a task to toggle.")
            return
        index = sel[0]
        text = self.listbox.get(index)
        task_text = text[4:]
        done = 0 if text[1] == "x" else 1
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE todo SET done=? WHERE task=?", (done, task_text))
        conn.commit()
        conn.close()
        self.load_tasks()

    def delete_task(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showwarning("Select Task", "Please select a task to delete.")
            return
        index = sel[0]
        text = self.listbox.get(index)
        task_text = text[4:]
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM todo WHERE task=?", (task_text,))
        conn.commit()
        conn.close()
        self.load_tasks()
