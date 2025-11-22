import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection
import datetime

class FeePage:
    def __init__(self):
        self.win = tk.Toplevel()
        self.win.title("Fees Module")
        self.win.geometry("900x650")
        self.win.configure(bg="#f0f0f0")

        tk.Label(self.win, text="Fees Management",
                 font=("Arial", 22, "bold"),
                 bg="#2c3e50", fg="white", pady=10).pack(fill="x")

        form = tk.Frame(self.win, bg="#ffffff", bd=2, relief="groove")
        form.pack(pady=10, padx=20)

        labels = ["Student ID", "Amount", "Month"]
        self.entries = {}
        for i,label in enumerate(labels):
            tk.Label(form,text=label,font=("Arial",12),bg="#ffffff",fg="#2c3e50").grid(row=i,column=0,padx=10,pady=5,sticky="w")
            entry = tk.Entry(form,width=25,bg="#ecf0f1")
            entry.grid(row=i,column=1,padx=10,pady=5)
            self.entries[label]=entry

        # Buttons
        btn_color="#3498db"
        btn_hover="#2980b9"
        def on_enter(e): e.widget['bg']=btn_hover
        def on_leave(e): e.widget['bg']=btn_color

        for i,(text,cmd) in enumerate([("Add Fee",self.add_fee),
                                       ("Update Fee",self.update_fee),
                                       ("Delete Fee",self.delete_fee)]):
            b=tk.Button(form,text=text,width=15,bg=btn_color,fg="white",command=cmd)
            b.grid(row=3,column=i,pady=10,padx=5)
            b.bind("<Enter>",on_enter)
            b.bind("<Leave>",on_leave)

        # Treeview
        self.tree=ttk.Treeview(self.win,columns=("ID","Student ID","Amount","Month","Date"),show="headings")
        style=ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",background="#ffffff",foreground="#2c3e50",
                        rowheight=25,fieldbackground="#ecf0f1")
        style.map("Treeview",background=[("selected","#3498db")],foreground=[("selected","white")])
        for col in self.tree["columns"]:
            self.tree.heading(col,text=col)
            self.tree.column(col,width=150)
        self.tree.pack(pady=20,fill="both",expand=True)
        self.tree.bind("<ButtonRelease-1>",self.load_selected_row)
        self.load_fees()

    # ---------- CRUD Methods ----------
    def run(self,query,params=()):
        conn=get_connection(); cur=conn.cursor(); cur.execute(query,params); conn.commit(); conn.close()
    def fetch(self,query):
        conn=get_connection(); cur=conn.cursor(); cur.execute(query); rows=cur.fetchall(); conn.close(); return rows

    def add_fee(self):
        student_id=self.entries["Student ID"].get()
        amount=self.entries["Amount"].get()
        month=self.entries["Month"].get()
        if not student_id.isdigit(): messagebox.showerror("Error","Enter valid Student ID"); return
        date=datetime.date.today().strftime("%Y-%m-%d")
        self.run("INSERT INTO fees(student_id,amount,month,date_issued) VALUES(?,?,?,?)",(student_id,amount,month,date))
        self.load_fees(); messagebox.showinfo("Success","Fee Added!")

    def load_fees(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        rows=self.fetch("SELECT * FROM fees")
        for row in rows: self.tree.insert("",tk.END,values=row)

    def load_selected_row(self,event):
        selected=self.tree.focus(); data=self.tree.item(selected,"values")
        if not data: return
        keys=["Student ID","Amount","Month"]
        for i,key in enumerate(keys): self.entries[key].delete(0,tk.END); self.entries[key].insert(0,data[i+1])
        self.current_id=data[0]

    def update_fee(self):
        if not hasattr(self,"current_id"): messagebox.showerror("Error","Select a fee"); return
        data=(self.entries["Student ID"].get(),
              self.entries["Amount"].get(),
              self.entries["Month"].get(),
              self.current_id)
        self.run("UPDATE fees SET student_id=?, amount=?, month=? WHERE fee_id=?",data)
        self.load_fees(); messagebox.showinfo("Updated","Fee Updated!")

    def delete_fee(self):
        if not hasattr(self,"current_id"): messagebox.showerror("Error","Select a fee"); return
        self.run("DELETE FROM fees WHERE fee_id=?",(self.current_id,))
        self.load_fees(); messagebox.showinfo("Deleted","Fee Deleted!")
