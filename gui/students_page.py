import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection

class StudentsPage:
    def __init__(self):
        self.win = tk.Toplevel()
        self.win.title("Student Management")
        self.win.geometry("900x650")
        self.win.configure(bg="#f0f0f0")

        tk.Label(self.win, text="Student Management",
                 font=("Arial", 22, "bold"),
                 bg="#2c3e50", fg="white", pady=10).pack(fill="x")

        form = tk.Frame(self.win, bg="#ffffff", bd=2, relief="groove")
        form.pack(pady=10, padx=20)

        labels = ["First Name", "Last Name", "Class", "Phone", "Parent Name"]
        self.entries = {}

        for i, label in enumerate(labels):
            tk.Label(form, text=label, font=("Arial", 12),
                     bg="#ffffff", fg="#2c3e50").grid(row=i, column=0, padx=10, pady=5, sticky="w")
            entry = tk.Entry(form, width=30, bg="#ecf0f1")
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries[label] = entry

        btn_color = "#3498db"
        btn_hover = "#2980b9"
        def on_enter(e): e.widget['bg'] = btn_hover
        def on_leave(e): e.widget['bg'] = btn_color

        for i, (text, cmd) in enumerate([("Add Student", self.add_student),
                                         ("Update Student", self.update_student),
                                         ("Delete Student", self.delete_student)]):
            b = tk.Button(form, text=text, width=15, bg=btn_color, fg="white", command=cmd)
            b.grid(row=6, column=i, pady=10, padx=5)
            b.bind("<Enter>", on_enter)
            b.bind("<Leave>", on_leave)

        self.tree = ttk.Treeview(self.win,
                                 columns=("ID","First Name","Last Name","Class","Phone","Parent"),
                                 show="headings")
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#ffffff", foreground="#2c3e50",
                        rowheight=25, fieldbackground="#ecf0f1")
        style.map("Treeview", background=[("selected","#3498db")], foreground=[("selected","white")])

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col,width=130)

        self.tree.pack(pady=20, fill="both", expand=True)
        self.tree.bind("<ButtonRelease-1>", self.load_selected_row)
        self.load_students()

    # -------------- CRUD Methods -----------------
    def run_query(self, query, params=()):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(query, params)
        conn.commit()
        conn.close()

    def fetch_query(self, query):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()
        return rows

    def add_student(self):
        data = (self.entries["First Name"].get(),
                self.entries["Last Name"].get(),
                self.entries["Class"].get(),
                self.entries["Phone"].get(),
                self.entries["Parent Name"].get())
        self.run_query("INSERT INTO students(first_name,last_name,student_class,phone,parent_name) VALUES(?,?,?,?,?)", data)
        self.load_students()
        messagebox.showinfo("Success","Student Added!")

    def load_students(self):
        for row in self.tree.get_children(): self.tree.delete(row)
        rows = self.fetch_query("SELECT * FROM students")
        for row in rows: self.tree.insert("",tk.END,values=row)

    def load_selected_row(self, event):
        selected = self.tree.focus()
        data = self.tree.item(selected,"values")
        if not data: return
        keys = ["First Name","Last Name","Class","Phone","Parent Name"]
        for i,key in enumerate(keys):
            self.entries[key].delete(0,tk.END)
            self.entries[key].insert(0,data[i+1])
        self.current_id = data[0]

    def update_student(self):
        if not hasattr(self,"current_id"): messagebox.showerror("Error","Select a student"); return
        data = (self.entries["First Name"].get(),
                self.entries["Last Name"].get(),
                self.entries["Class"].get(),
                self.entries["Phone"].get(),
                self.entries["Parent Name"].get(),
                self.current_id)
        self.run_query("UPDATE students SET first_name=?, last_name=?, student_class=?, phone=?, parent_name=? WHERE student_id=?", data)
        self.load_students()
        messagebox.showinfo("Updated","Student Updated!")

    def delete_student(self):
        if not hasattr(self,"current_id"): messagebox.showerror("Error","Select a student"); return
        self.run_query("DELETE FROM students WHERE student_id=?",(self.current_id,))
        self.load_students()
        messagebox.showinfo("Deleted","Student Deleted!")
