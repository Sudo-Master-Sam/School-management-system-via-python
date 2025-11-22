import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection
import datetime

class AttendancePage:
    def __init__(self):
        self.win = tk.Toplevel()
        self.win.title("Teacher Attendance")
        self.win.geometry("900x650")
        self.win.configure(bg="#f0f0f0")

        tk.Label(self.win,text="Teacher Attendance",font=("Arial",22,"bold"),
                 bg="#2c3e50",fg="white",pady=10).pack(fill="x")

        # Form Frame
        form = tk.Frame(self.win,bg="#ffffff",bd=2,relief="groove")
        form.pack(pady=10,padx=20)

        tk.Label(form,text="Teacher ID:",font=("Arial",12),bg="#ffffff",fg="#2c3e50").grid(row=0,column=0,padx=10,pady=5,sticky="w")
        self.teacher_id_entry = tk.Entry(form,width=25,bg="#ecf0f1")
        self.teacher_id_entry.grid(row=0,column=1)

        tk.Label(form,text="Date (YYYY-MM-DD):",font=("Arial",12),bg="#ffffff",fg="#2c3e50").grid(row=1,column=0,padx=10,pady=5,sticky="w")
        self.date_entry = tk.Entry(form,width=25,bg="#ecf0f1")
        self.date_entry.grid(row=1,column=1)
        self.date_entry.insert(0, datetime.date.today().strftime("%Y-%m-%d"))

        tk.Label(form,text="Status:",font=("Arial",12),bg="#ffffff",fg="#2c3e50").grid(row=2,column=0,padx=10,pady=5,sticky="w")
        self.status_combobox = ttk.Combobox(form,values=["Present","Absent"],width=22)
        self.status_combobox.current(0)
        self.status_combobox.grid(row=2,column=1)

        # Buttons
        btn_color="#3498db"
        btn_hover="#2980b9"
        def hover_enter(e): e.widget['bg']=btn_hover
        def hover_leave(e): e.widget['bg']=btn_color

        add_btn = tk.Button(form,text="Mark Attendance",width=20,bg=btn_color,fg="white",command=self.mark_attendance)
        add_btn.grid(row=3,column=0,pady=10,padx=5)
        add_btn.bind("<Enter>",hover_enter)
        add_btn.bind("<Leave>",hover_leave)

        delete_btn = tk.Button(form,text="Delete Record",width=20,bg=btn_color,fg="white",command=self.delete_attendance)
        delete_btn.grid(row=3,column=1,pady=10,padx=5)
        delete_btn.bind("<Enter>",hover_enter)
        delete_btn.bind("<Leave>",hover_leave)

        # Treeview
        self.tree=ttk.Treeview(self.win,columns=("ID","Teacher ID","Date","Status"),show="headings")
        style=ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",background="#ffffff",foreground="#2c3e50",rowheight=25,fieldbackground="#ecf0f1")
        style.map("Treeview",background=[("selected","#3498db")],foreground=[("selected","white")])

        for col in self.tree["columns"]:
            self.tree.heading(col,text=col)
            self.tree.column(col,width=150)
        self.tree.pack(pady=20,fill="both",expand=True)
        self.tree.bind("<ButtonRelease-1>",self.load_selected_row)

        self.load_attendance()

    # ---------- Database Methods ----------
    def run_query(self,query,params=()):
        conn=get_connection(); cur=conn.cursor(); cur.execute(query,params); conn.commit(); conn.close()

    def fetch_query(self,query,params=()):
        conn=get_connection(); cur=conn.cursor(); cur.execute(query,params); rows=cur.fetchall(); conn.close(); return rows

    # ---------- CRUD ----------
    def mark_attendance(self):
        teacher_id=self.teacher_id_entry.get()
        date=self.date_entry.get()
        status=self.status_combobox.get()
        if not teacher_id.isdigit(): messagebox.showerror("Error","Enter valid Teacher ID"); return
        self.run_query("INSERT INTO teacher_attendance(teacher_id,date,status) VALUES(?,?,?)",(teacher_id,date,status))
        self.load_attendance()
        messagebox.showinfo("Success","Attendance marked!")

    def load_attendance(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        rows=self.fetch_query("SELECT * FROM teacher_attendance ORDER BY date DESC")
        for row in rows: self.tree.insert("",tk.END,values=row)

    def load_selected_row(self,event):
        selected=self.tree.focus()
        data=self.tree.item(selected,"values")
        if not data: return
        self.current_id=data[0]
        self.teacher_id_entry.delete(0,tk.END)
        self.teacher_id_entry.insert(0,data[1])
        self.date_entry.delete(0,tk.END)
        self.date_entry.insert(0,data[2])
        self.status_combobox.set(data[3])

    def delete_attendance(self):
        if not hasattr(self,"current_id"): messagebox.showerror("Error","Select a record"); return
        self.run_query("DELETE FROM teacher_attendance WHERE attendance_id=?",(self.current_id,))
        self.load_attendance()
        messagebox.showinfo("Deleted","Attendance record deleted!")
