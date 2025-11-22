import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from database import get_connection

class ReceiptsPage:
    def __init__(self):
        self.win = tk.Toplevel()
        self.win.title("Receipts")
        self.win.geometry("950x650")
        self.win.configure(bg="#f0f0f0")

        tk.Label(self.win,text="Receipts Manager",font=("Arial",22,"bold"),
                 bg="#2c3e50",fg="white",pady=10).pack(fill="x")

        filter_frame = tk.Frame(self.win,bg="#ffffff",bd=2,relief="groove")
        filter_frame.pack(pady=10,padx=20)

        tk.Label(filter_frame,text="Student ID:",font=("Arial",12),bg="#ffffff",fg="#2c3e50").grid(row=0,column=0,padx=10)
        self.search_id = tk.Entry(filter_frame,width=15,bg="#ecf0f1")
        self.search_id.grid(row=0,column=1)

        btn_color="#3498db"
        btn_hover="#2980b9"
        def on_enter(e): e.widget['bg']=btn_hover
        def on_leave(e): e.widget['bg']=btn_color

        tk.Button(filter_frame,text="Search",width=12,bg=btn_color,fg="white",command=self.search_receipts).grid(row=0,column=2,padx=10)
        tk.Button(filter_frame,text="Clear Filters",width=12,bg=btn_color,fg="white",command=self.load_receipts).grid(row=0,column=3,padx=10)
        tk.Button(filter_frame,text="Apply Filter",width=12,bg=btn_color,fg="white",command=self.filter_type).grid(row=1,column=2,padx=10)

        for b in filter_frame.winfo_children():
            if isinstance(b, tk.Button): b.bind("<Enter>",on_enter); b.bind("<Leave>",on_leave)

        tk.Label(filter_frame,text="Filter Type:",font=("Arial",12),bg="#ffffff",fg="#2c3e50").grid(row=1,column=0,padx=10)
        self.type_filter=ttk.Combobox(filter_frame,values=["All","Fee","Uniform","Stationery"],width=12)
        self.type_filter.current(0); self.type_filter.grid(row=1,column=1)

        self.tree = ttk.Treeview(self.win,
                                 columns=("ID","Student","Type","Details","Amount","Date"),
                                 show="headings")
        style=ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",background="#ffffff",foreground="#2c3e50",
                        rowheight=25,fieldbackground="#ecf0f1")
        style.map("Treeview",background=[("selected","#3498db")],foreground=[("selected","white")])
        for col in self.tree["columns"]:
            self.tree.heading(col,text=col)
            self.tree.column(col,width=150)
        self.tree.pack(pady=20,fill="both",expand=True)

        tk.Button(self.win,text="Export Selected Receipt",width=25,bg=btn_color,fg="white",command=self.export_receipt).pack(pady=10).bind("<Enter>",on_enter).bind("<Leave>",on_leave)

        self.load_receipts()

    # ---------- Database Methods ----------
    def fetch(self, query, params=()):
        conn=get_connection(); cur=conn.cursor(); cur.execute(query,params); rows=cur.fetchall(); conn.close(); return rows

    def load_receipts(self):
        self.update_table(self.fetch("SELECT * FROM receipts"))

    def update_table(self,rows):
        for i in self.tree.get_children(): self.tree.delete(i)
        for row in rows: self.tree.insert("",tk.END,values=row)

    # ---------- Filters ----------
    def search_receipts(self):
        student_id=self.search_id.get()
        if not student_id.isdigit(): messagebox.showerror("Error","Enter valid Student ID"); return
        result=self.fetch("SELECT * FROM receipts WHERE student_id=?",(student_id,))
        self.update_table(result)

    def filter_type(self):
        t=self.type_filter.get()
        if t=="All": self.load_receipts(); return
        result=self.fetch("SELECT * FROM receipts WHERE type=?",(t,))
        self.update_table(result)

    # ---------- Export ----------
    def export_receipt(self):
        selected=self.tree.focus()
        data=self.tree.item(selected,"values")
        if not data: messagebox.showwarning("Warning","Select a receipt first!"); return
        receipt_text=(f"Receipt ID: {data[0]}\nStudent ID: {data[1]}\nType: {data[2]}\nDetails: {data[3]}\nAmount: {data[4]}\nDate: {data[5]}\n")
        file_path=filedialog.asksaveasfilename(defaultextension=".txt",filetypes=[("Text Files","*.txt")])
        if file_path:
            with open(file_path,"w") as f: f.write(receipt_text)
            messagebox.showinfo("Success","Receipt exported successfully!")
