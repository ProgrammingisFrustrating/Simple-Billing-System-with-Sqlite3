from tkinter import *
from tkinter import ttk
import sqlite3

class soft:
    def __init__(self, root):
        self.root = root
        self.root.title('DEMO')
        self.root.geometry('%dx%d+0+0' % (width_value, height_value))

        title = Label(self.root, text='DEMO', font=('times new roman', 40, 'bold'), bg='coral')
        title.pack(fill=X)

    #================creating database==============#
        self.conn = sqlite3.connect('Rate.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS Rate(
                        Serial_num NUMERIC,
                        HSN_Num TEXT,
                        Item_Name TEXT,
                        MRP NUMERIC,
                        Dealer_Price NUMERIC,
                        Customer_Price NUMERIC,
                        PRIMARY KEY (Serial_num)
                        )''')

    #=================Creating Variable==============#
        self.serial_no = StringVar()
        self.hsn_no = StringVar()
        self.item_name = StringVar()
        self.mrp = StringVar()
        self.dealer = StringVar()
        self.customer = StringVar()

        self.search_by = StringVar()
        self.search_txt = StringVar()
        
    #==============top bar=================#
        Search = Frame(self.root, bd=4, relief=RIDGE, bg='gray')
        Search.place(x=15, y=80, width=1500, height=80)
        
        lbl_ser = Label(Search, text='Serial Nmber', bg="gray", font=('times new roman', 20, 'bold'))
        lbl_ser.grid(row=0, column=0, pady=10, padx=30, sticky='w')
        
        txt_ser = Entry(Search, font=('times new roman', 16, 'bold'), textvariable=self.serial_no, width=15,  bd=5, relief=GROOVE)
        txt_ser.grid(row=0, column=1, pady=17, padx=10, sticky='w')

        btn = Button(Search, text='Dealer Search', width=20, height=2, command=self.dealer_search).grid(row=0, column=2, padx=30, pady=17)
        btn = Button(Search, text='Customer Search', width=20, height=2, command=self.custmer_search).grid(row=0, column=3, padx=5, pady=17)
        add_btn = Button(Search, text='Add/Remove', width=20, height=2, command=self.open).grid(row=0, column=4, padx=30, pady=17)

    #=====================Display Table=============#
        Table_frame = Frame(root, bd=4, relief=RIDGE, bg='gray')
        Table_frame.place(x=15, y=170, width=1500, height=615)

        scroll_x = Scrollbar(Table_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(Table_frame, orient=VERTICAL)
        self.item_table = ttk.Treeview(Table_frame, column=('Serial No', 'HSN No', 'Item Name', 'MRP', 'Price'),
                                       xscrollcommand=scroll_x,
                                       yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.item_table.xview)
        scroll_y.config(command=self.item_table.yview)

        self.item_table.heading('Serial No', text='Serial No')
        self.item_table.heading('HSN No', text='HSN No')
        self.item_table.heading('Item Name', text='Item Name')
        self.item_table.heading('MRP', text='MRP')
        self.item_table.heading('Price', text='Price')
        self.item_table['show'] = 'headings'
        self.item_table.column('Serial No', width=1)
        self.item_table.column('HSN No', width=5)
        self.item_table.column('Item Name', width=2)
        self.item_table.column('MRP', width=10)
        self.item_table.column('Price', width=10)
        self.item_table.pack(fill=BOTH, expand=1)
        self.fetch_data2()

    def dealer_search(self):
        with self.conn:
            self.c.execute('SELECT Serial_num, HSN_Num, Item_Name, MRP, Dealer_Price FROM Rate WHERE Serial_num=:serial',
                           {'serial':self.serial_no.get()})
            rows = self.c.fetchall()
            if len(rows) != 0:
                self.item_table.delete(*self.item_table.get_children())
                for row in rows:
                    self.item_table.insert('', END, values=row)

    def custmer_search(self):
        with self.conn:
            self.c.execute('SELECT Serial_num, HSN_Num, Item_Name, MRP, Customer_Price FROM Rate WHERE Serial_num=:serial',
                           {'serial':self.serial_no.get()})
            rows = self.c.fetchall()
            if len(rows) != 0:
                self.item_table.delete(*self.item_table.get_children())
                for row in rows:
                    self.item_table.insert('', END, values=row)


    def open(self):
        top = Toplevel()
        top.title('Add/Remove')
        top.geometry('1100x700+0+0')

    #=================Details filling=============#
        detail_frame = Frame(top, bd=4, relief=RIDGE, bg='alice blue')
        detail_frame.place(x=20, y=20, width=460, height=655)

        title = Label(detail_frame, text='Detail', bg='alice blue', font=('times new roman', 30, 'bold'))
        title.grid(row=0, columnspan=2, pady=20, padx=10)

        lbl_ser = Label(detail_frame, text='Serial Num', bg='alice blue', font=('times new roman', 22, 'bold'))
        lbl_ser.grid(row=1, column=0, pady=20, padx=5)
        txt_ser = Entry(detail_frame, textvariable=self.serial_no, font=('times new roman', 15, 'bold'), bd=5, relief=GROOVE)
        txt_ser.grid(row=1, column=1, pady=5, padx=15, sticky='w')

        lbl_hsn = Label(detail_frame, text='HSN Num', bg='alice blue', font=('times new roman', 22, 'bold'))
        lbl_hsn.grid(row=2, column=0, pady=20, padx=5)
        txt_hsn = Entry(detail_frame, textvariable=self.hsn_no, font=('times new roman', 15, 'bold'), bd=5, relief=GROOVE)
        txt_hsn.grid(row=2, column=1, pady=5, padx=15, sticky='w')

        lbl_name = Label(detail_frame, text='Item Name', bg='alice blue', font=('times new roman', 22, 'bold'))
        lbl_name.grid(row=3, column=0, pady=20, padx=5)
        txt_name = Entry(detail_frame, textvariable=self.item_name, font=('times new roman', 15, 'bold'), bd=5, relief=GROOVE)
        txt_name.grid(row=3, column=1, pady=5, padx=15, sticky='w')

        lbl_mrp = Label(detail_frame, text='MRP', bg='alice blue', font=('times new roman', 22, 'bold'))
        lbl_mrp.grid(row=4, column=0, pady=20, padx=5)
        txt_mrp = Entry(detail_frame, textvariable=self.mrp, font=('times new roman', 15, 'bold'), bd=5, relief=GROOVE)
        txt_mrp.grid(row=4, column=1, pady=5, padx=15, sticky='w')

        lbl_dealer = Label(detail_frame, text='Dealer Price', bg='alice blue', font=('times new roman', 22, 'bold'))
        lbl_dealer.grid(row=5, column=0, pady=20, padx=5)
        txt_dealer = Entry(detail_frame, textvariable=self.dealer, font=('times new roman', 15, 'bold'), bd=5, relief=GROOVE)
        txt_dealer.grid(row=5, column=1, pady=5, padx=15, sticky='w')

        lbl_customer = Label(detail_frame, text='Customer Price', bg='alice blue', font=('times new roman', 22, 'bold'))
        lbl_customer.grid(row=6, column=0, pady=20, padx=10)
        txt_customer = Entry(detail_frame, textvariable=self.customer, font=('times new roman', 15, 'bold'), bd=5, relief=GROOVE)
        txt_customer.grid(row=6, column=1, pady=5, padx=15, sticky='w')

    # ===================Button Frame=============================#
        btn_frame = Frame(detail_frame, bd=4, relief=RIDGE, bg='alice blue')
        btn_frame.place(x=17, y=570, width=420)

        addbtn = Button(btn_frame, text='Add', width=10, command=self.add_item).grid(row=0, column=0, padx=15, pady=10)
        updatebtn = Button(btn_frame, text='Update', width=10, command=self.update).grid(row=0, column=1, padx=10, pady=10)
        deletebtn = Button(btn_frame, text='Delete', width=10, command=self.delete).grid(row=0, column=2, padx=10, pady=10)
        clearbtn = Button(btn_frame, text='Clear', width=10, command=self.clear).grid(row=0, column=3, padx=5, pady=10)

    #====================Display frame===============#
        disp_frame = Frame(top, bd=4, relief=RIDGE, bg='alice blue')
        disp_frame.place(x=500, y=20, width=575, height=655)

        lbl_search = Label(disp_frame, text='Search By', bg="alice blue", font=('times new roman', 16, 'bold'))
        lbl_search.grid(row=0, column=0, pady=15, padx=20, sticky='w')

        combo_gen = ttk.Combobox(disp_frame, textvariable=self.search_by, font=('times new roman', 10, 'bold'), state='readonly')
        combo_gen['values'] = ('Serial_num', 'HSN_Num', 'Item_Name')
        combo_gen.grid(row=1, column=0, pady=5, padx=20)

        txt_s = Entry(disp_frame, font=('times new roman', 10, 'bold'), textvariable=self.search_txt, bd=5, relief=GROOVE)
        txt_s.grid(row=1, column=1, pady=5, padx=5)

        searchbtn = Button(disp_frame, text='Search', width=10, command=self.search).grid(row=1, column=2, padx=10, pady=2)
        searchAllbtn = Button(disp_frame, text='Search All', width=10, command=self.fetch_data).grid(row=1, column=3, padx=10, pady=2)

    #============= Display Screen=============#
        t_frame = Frame(disp_frame, bd=4, relief=RIDGE, bg='alice blue')
        t_frame.place(x=5, y=100, width=557, height=543)

        scroll_x = Scrollbar(t_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(t_frame, orient=VERTICAL)
        self.create_table = ttk.Treeview(t_frame, column=('Serial No', 'HSN No', 'Item Name', 'MRP', 'Dealer Price', 'Customer Price'),
                                       xscrollcommand=scroll_x,
                                       yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.create_table.xview)
        scroll_y.config(command=self.create_table.yview)

        self.create_table.heading('Serial No', text='Serial No')
        self.create_table.heading('HSN No', text='HSN No')
        self.create_table.heading('Item Name', text='Item Name')
        self.create_table.heading('MRP', text='MRP')
        self.create_table.heading('Dealer Price', text='Dealer Price')
        self.create_table.heading('Customer Price', text='Customer Price')
        self.create_table['show'] = 'headings'
        self.create_table.column('Serial No', width=5)
        self.create_table.column('HSN No', width=5)
        self.create_table.column('Item Name', width=5)
        self.create_table.column('MRP', width=5)
        self.create_table.column('Dealer Price', width=5)
        self.create_table.column('Customer Price', width=5)
        self.create_table.pack(fill=BOTH, expand=1)
        self.create_table.bind('<ButtonRelease-1>', self.get_cursor)
        self.fetch_data()

    def add_item(self):
        with self.conn:
            self.c.execute('INSERT INTO Rate VALUES(:serial, :hsn, :item, :mrp, :dealer, :customer)',
                           {'serial':self.serial_no.get(),
                            'hsn':self.hsn_no.get(),
                            'item':self.item_name.get(),
                            'mrp':self.mrp.get(),
                            'dealer':self.dealer.get(),
                            'customer':self.customer.get()})
            self.fetch_data()
            self.fetch_data2()
            self.clear()

    def fetch_data(self):
        with self.conn:
            self.c.execute('SELECT * FROM Rate')
            rows = self.c.fetchall()
            if len(rows)!=0:
                self.create_table.delete(*self.create_table.get_children())
                for row in rows:
                    self.create_table.insert('', END, values=row)

    def fetch_data2(self):
        with self.conn:
            self.c.execute('SELECT * FROM Rate')
            rows = self.c.fetchall()
            if len(rows)!=0:
                self.item_table.delete(*self.item_table.get_children())
                for row in rows:
                    self.item_table.insert('', END, values=row)

    def clear(self):
        with self.conn:
            self.serial_no.set('')
            self.hsn_no.set('')
            self.item_name.set('')
            self.mrp.set('')
            self.dealer.set('')
            self.customer.set('')

    def get_cursor(self, r):
        with self.conn:
            cur = self.create_table.focus()
            content = self.create_table.item(cur)
            row = content['values']
            self.serial_no.set(row[0])
            self.hsn_no.set(row[1])
            self.item_name.set(row[2])
            self.mrp.set(row[3])
            self.dealer.set(row[4])
            self.customer.set(row[5])

    def update(self):
        with self.conn:
            self.c.execute('UPDATE Rate SET HSN_Num=:hsn, Item_Name=:item, MRP=:mrp, Dealer_Price=:dealer, Customer_Price=:customer WHERE Serial_num=:serial',
                           {'serial': self.serial_no.get(),
                            'hsn': self.hsn_no.get(),
                            'item': self.item_name.get(),
                            'mrp': self.mrp.get(),
                            'dealer': self.dealer.get(),
                            'customer': self.customer.get()})
            self.fetch_data()
            self.clear()
            
    def delete(self):
        with self.conn:
            self.c.execute('DELETE FROM Rate WHERE Serial_num=:serial', {'serial':self.serial_no.get()})
            self.fetch_data()
            self.clear()

    def search(self):
        with self.conn:
            self.c.execute("select * from Rate where " + str(self.search_by.get()) + " LIKE '%" + str(self.search_txt.get()) + "%'")
            rows = self.c.fetchall()
            if len(rows) != 0:
                self.create_table.delete(*self.create_table.get_children())
                for row in rows:
                    self.create_table.insert('', END, values=row)


root = Tk()
width_value = root.winfo_screenwidth()
height_value = root.winfo_screenheight()
ob = soft(root)
root.mainloop()
