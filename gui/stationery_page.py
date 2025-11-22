import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection
import datetime

class StationeryPage:
    def __init__(self):
        self.win = tk.Toplevel()
        self.win.title("Stationery Inventory")
        self.win.geometry("900x650")
        self.win.configure(bg="#f0f0f0")

        tk.Label(self.win,text="Stationery Inventory",font=("Arial",22,"bold"),
                 bg="#2c3e50",fg="white",pady=10).pack(fill="x")

        form = tk.Frame(self.win,bg="#ffffff",bd=2,relief="groove")
        form.pack(pady=10,padx=20)

        labels=["Item Name","Quantity","Price"]
        self.entries={}
        for i,label in enumerate(labels):
            tk.Label(form,text=label,font=("Arial",12),
                     bg="#ffffff",fg="#2c3e50").grid(row=i,column=0,padx=10,pady=5,sticky="w")
            entry = tk.Entry(form,width=25,bg="#ecf0f1")
            entry.grid(row=i,column=1,padx=10,pady=5)
            self.entries[label]=entry

        # Buttons
        btn_color="#3498db"
        btn_hover="#2980b9"
        def on_enter(e): e.widget['bg']=btn_hover
        def on_leave(e): e.widget['bg']=btn_color

        for i,(text,cmd) in enumerate([("Add Item",self.add_item),
                                       ("Update Item",self.update_item),
                                       ("Delete Item",self.delete_item)]):
            b = tk.Button(form,text=text,width=15,bg=btn_color,fg="white",command=cmd)
            b.grid(row=4,column=i,pady=10,padx=5)
            b.bind("<Enter>",on_enter)
            b.bind("<Leave>",on_leave)

        # Issue to student
        tk.Label(form,text="Student ID:",font=("Arial",12),bg="#ffffff",fg="#2c3e50").grid(row=5,column=0,pady=10)
        self.student_id_entry = tk.Entry(form,width=25,bg="#ecf0f1")
        self.student_id_entry.grid(row=5,column=1)
        b = tk.Button(form,text="Issue Item",width=15,bg=btn_color,fg="white",command=self.issue_stationery)
        b.grid(row=5,column=2)
        b.bind("<Enter>",on_enter); b.bind("<Leave>",on_leave)

        # Treeview
        self.tree=ttk.Treeview(self.win,columns=("ID","Item","Qty","Price"),show="headings")
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
        self.load_items()

    # ---------- CRUD & Issue Methods ----------
    def run(self, query, params=()):
        conn=get_connection(); cur=conn.cursor(); cur.execute(query,params); conn.commit(); conn.close()
    def fetch(self, query):
        conn=get_connection(); cur=conn.cursor(); cur.execute(query); rows=cur.fetchall(); conn.close(); return rows

    def add_item(self):
        data=(self.entries["Item Name"].get(),
              self.entries["Quantity"].get(),
              self.entries["Price"].get())
        self.run("INSERT INTO stationery(item_name,quantity,price) VALUES(?,?,?)",data)
        self.load_items(); messagebox.showinfo("Success","Item Added!")

    def load_items(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        rows=self.fetch("SELECT * FROM stationery")
        for row in rows: self.tree.insert("",tk.END,values=row)

    def load_selected_row(self,event):
        selected=self.tree.focus(); data=self.tree.item(selected,"values")
        if not data: return
        keys=["Item Name","Quantity","Price"]
        for i,key in enumerate(keys): self.entries[key].delete(0,tk.END); self.entries[key].insert(0,data[i+1])
        self.current_id=data[0]

    def update_item(self):
        if not hasattr(self,"current_id"): messagebox.showerror("Error","Select an item"); return
        data=(self.entries["Item Name"].get(),
              self.entries["Quantity"].get(),
              self.entries["Price"].get(),
              self.current_id)
        self.run("UPDATE stationery SET item_name=?, quantity=?, price=? WHERE item_id=?",data)
        self.load_items(); messagebox.showinfo("Updated","Item Updated!")

    def delete_item(self):
        if not hasattr(self,"current_id"): messagebox.showerror("Error","Select an item"); return
        self.run("DELETE FROM stationery WHERE item_id=?",(self.current_id,))
        self.load_items(); messagebox.showinfo("Deleted","Item Deleted!")

    def issue_stationery(self):
        if not hasattr(self,"current_id"): messagebox.showerror("Error","Select an item"); return
        student_id=self.student_id_entry.get()
        if not student_id.isdigit(): messagebox.showerror("Error","Enter valid Student ID"); return
        rows=self.fetch(f"SELECT item_name, quantity, price FROM stationery WHERE item_id={self.current_id}")
        item_name, qty, price = rows[0]
        if qty<=0: messagebox.showerror("Error","Item out of stock"); return
        self.run("UPDATE stationery SET quantity = quantity - 1 WHERE item_id=?",(self.current_id,))
        date=datetime.date.today().strftime("%Y-%m-%d")
        self.run("INSERT INTO receipts(student_id,type,item_details,total_amount,date_issued) VALUES(?, 'Stationery', ?, ?, ?)",
                 (student_id,item_name,price,date))
        self.load_items(); messagebox.showinfo("Success","Item issued and receipt created!")
