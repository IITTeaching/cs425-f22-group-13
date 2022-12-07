from asyncio.windows_events import NULL
from pickle import FALSE
import tkinter as tk
import psycopg2
from decimal import Decimal
import random


#        conn = psycopg2.connect("dbname=bank user=bob password=password123")
#   cur = conn.cursor()
#   cur.execute("SELECT * FROM branches;")
#   print(cur.fetchone())
class MainFrame(tk.Tk):
    #Frame object holding all pages
    cont = None
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("750x350")

        container = tk.Frame(self)
        container.pack(fill='both', expand=1)
        self.get_initial_data()

        self.listing = {}

        for p in (LoginPage, EmployeePage, TellerLogin, ManagerLogin, CustomerLogin) :
            page_name = p.__name__
            frame = p(parent = container, controller = self)
            frame.place(relheight=1, relwidth=1)
            self.listing[page_name] = frame
        self.up_frame('LoginPage')
    tellers = []
    managers = []
    customers = []
    def get_initial_data(self):
        conn = psycopg2.connect(user="bob",password="password123",host="127.0.0.1",port="5432",database="bank")
        cur = conn.cursor()
        cur.execute("SELECT name FROM Employees WHERE type = 'Teller';")
        tellers = cur.fetchall()
        print(tellers)
        self.tellers = tellers
        cur.execute("SELECT name FROM Employees WHERE type = 'Manager';")
        managers = cur.fetchall()
        print(managers)
        self.managers = managers
        cur.execute("SELECT name FROM Customers;")
        cust = cur.fetchall()
        self.customers = cust
        cur.close()
        conn.close()

    def get_teller_acc(self):
        conn = psycopg2.connect(user="john",password="password456",host="127.0.0.1",port="5432",database="bank")
        cur = conn.cursor()
        cur.execute("SELECT number FROM Account;")
        accounts = cur.fetchall()
        cur.close()
        conn.close()
        return accounts
    

    def get_cust_acc(self, name):
        conn = psycopg2.connect("dbname=bank user=sam password=password789")
        cur = conn.cursor()
        cur.execute("SELECT number FROM (SELECT * FROM (SELECT * FROM owns NATURAL JOIN customers) as sub1 WHERE name = '" + name +  "') as sub2;")
        accounts = cur.fetchall()
        cur.close()
        conn.close()
        return accounts

    def get_manager_acc(self):
        conn = psycopg2.connect(user="bob",password="password123",host="127.0.0.1",port="5432",database="bank")
        cur = conn.cursor()
        cur.execute("SELECT number FROM Account;")
        accounts = cur.fetchall()
        cur.close()
        conn.close()
        return accounts

    def manager_acc_man(self, action): ###BOOKMARK CTRL-F TO GET HERE!!
        if action == 'create':
            def get_acc_id():
                id = ''
                for i in range(0, 10):
                    id += str(random.randint(0, 9))
                return id
            def exec_create():
                prompt.pack_forget()
                numbers.pack_forget()
                type_drop.pack_forget()
                conf_btn.pack_forget()
                conn = psycopg2.connect(user="bob",password="password123",host="127.0.0.1",port="5432",database="bank")
                cur = conn.cursor()
                id_uniq = False
                while not id_uniq:
                    id = get_acc_id()
                    cur.execute("SELECT Number FROM Account WHERE Number = '" + id + "'")
                    check_uniq = cur.fetchall()
                    if check_uniq == []:
                        id_uniq = True
                ssn_string = numbers.get('1.0','end-1c')
                ssn_list = ssn_string.split()
                cur.execute("INSERT INTO Account VALUES ('" + id +"', '" + type_choice.get() + "', 0.00)")
                for i in range(len(ssn_list)):
                    print(ssn_list[i])
                    cur.execute("INSERT INTO Owns VALUES ('"+ ssn_list[i] + "', '" + id +"')")

                conn.commit()
                cur.close()
                conn.close()
                conf_message = tk.Label(self, text='Account created with account ID ' + id + ' and owners ' + ssn_string)
                conf_message.pack()
                #Check if SSNs are valid?


            prompt = tk.Label(self, text='Please enter SSN of account owner. For joint accounts, separate SSN entries with spaces.')
            prompt.pack()
            #acc_prompt.place(x=270,y=20)

            numbers = tk.Text(self, height = 1,
             width = 33,
             bg = "white",
             fg="red")
            numbers.pack()

            options = ['Checking', 'Savings']
            type_choice = tk.StringVar()
            type_choice.set(options[0])
            type_drop = tk.OptionMenu(self, type_choice, *options)
            type_drop.pack()

            conf_btn = tk.Button(self, text='Create', command= lambda: exec_create())
            conf_btn.pack()

        elif action == 'delete':
            def exec_delete():
                prompt.pack_forget()
                del_drop.pack_forget()
                conf_btn.pack_forget()
                conn = psycopg2.connect(user="bob",password="password123",host="127.0.0.1",port="5432",database="bank")
                cur = conn.cursor()
                cur.execute("DELETE FROM Owns WHERE Number = '" + del_acc.get() + "'")
                cur.execute("DELETE FROM Account WHERE Number = '" + del_acc.get() + "'")
                conn.commit()
                cur.close()
                conn.close()
                conf_message = tk.Label(self, text='Account with ID ' + del_acc.get() + "' deleted.")
                conf_message.pack()
            prompt = tk.Label(self, text='Please select account to be deleted.')
            prompt.pack()

            acc = self.get_manager_acc()
            print(acc)
            acc_list = []
            for i in acc:
                for x in i:
                    print(x)
                    acc_list.append(x)
            del_acc = tk.StringVar()
            del_acc.set(acc_list[0])
            del_drop = tk.OptionMenu(self, del_acc, *acc_list)
            del_drop.pack()

            conf_btn = tk.Button(self, text='Delete', command= lambda: exec_delete())
            conf_btn.pack()
        
    
    def choose_ana(self, analytic):
        success_msg = tk.Label(self, text='',fg="green")
        if analytic == 'networth':
            conn = psycopg2.connect(user="bob",password="password123",host="127.0.0.1",port="5432",database="bank")
            cur = conn.cursor()
            get_net = "SELECT SUM(Balance) AS sum FROM Account"
            cur.execute(get_net)
            net = cur.fetchall()
            success_msg.pack()
            success_msg.place(x=280, y=200)
            success_msg.config(text="Total Net Worth: " + str(net[0][0]))
            # success_msg.config(text=net)
            conn.commit()
            cur.close()
            conn.close()
        elif analytic == 'mean':
            conn = psycopg2.connect(user="bob",password="password123",host="127.0.0.1",port="5432",database="bank")
            cur = conn.cursor()
            get_avg = "SELECT AVG(Balance) AS mean FROM Account"
            cur.execute(get_avg)
            mean = cur.fetchall()
            success_msg.pack()
            success_msg.place(x=255, y=200)
            success_msg.config(text="Mean of Balances: " + str(mean[0][0]))
            conn.commit()
            cur.close()
            conn.close()
        elif analytic == 'mostvaluable': #SELECT Number,Balance FROM Account ORDER BY Balance DESC LIMIT 1
            conn = psycopg2.connect(user="bob",password="password123",host="127.0.0.1",port="5432",database="bank")
            cur = conn.cursor()
            get_mst = "SELECT Number,Balance FROM Account ORDER BY Balance DESC LIMIT 1"
            cur.execute(get_mst)
            mst = cur.fetchall()
            success_msg.pack()
            success_msg.place(x=200, y=200)
            success_msg.config(text="Most Valuable Account: " + str(mst[0][0]) + " with a balance of " + str(mst[0][1]))
            conn.commit()
            cur.close()
            conn.close()
        elif analytic == 'leastvaluable':
            conn = psycopg2.connect(user="bob",password="password123",host="127.0.0.1",port="5432",database="bank")
            cur = conn.cursor()
            get_lst = "SELECT Number,Balance FROM Account ORDER BY Balance ASC LIMIT 1"
            cur.execute(get_lst)
            lst = cur.fetchall()
            success_msg.pack()
            success_msg.place(x=200, y=200)
            success_msg.config(text="Least Valuable Account: " + str(lst[0][0]) + " with a balance of " + str(lst[0][1]))
            conn.commit()
            cur.close()
            conn.close()
    
    
    def choose_acc(self, transfer, loggedInAcc, loggedInAs):
        def loop(a):
            print(a)
            for i in a:
                for x in i:
                    return x
        def get_trans_id():
            id = ''
            for i in range(0, 20):
                id += str(random.randint(0, 9))
            return id


        incor_inp = tk.Label(self, text='', fg="red")
        success_msg = tk.Label(self, text='',fg="green")
        def Take_input():
            if bool(success_msg.winfo_ismapped()) == True:
                success_msg.config(text='')
            if bool(incor_inp.winfo_ismapped()) == True:
                print('err = true')
                incor_inp.config(text="")
            INPUT = inputtxt.get("1.0", "end-1c")
            print(INPUT)
            if(INPUT.isdecimal() == False):
                incor_inp.pack()
                incor_inp.place(x=200, y=200)
                incor_inp.config(text='Incorrect Input, please make sure you entered a number')
            else:
                if transfer == 'transfer':
                    conn = psycopg2.connect(user="john",password="password456",host="127.0.0.1",port="5432",database="bank")
                    cur = conn.cursor()
                    get_curr_bal = "SELECT balance FROM Account WHERE number = " + "'" + clicked.get() + "'"
                    cur.execute(get_curr_bal)
                    x = loop(cur.fetchall())
                    newVal = x-Decimal(INPUT)
                    update_val = "UPDATE Account SET balance=" + str(newVal) + " WHERE number = '" + clicked.get() + "';"
                    cur.execute(update_val)
                    conn.commit()
                    get_curr_bal_2 = "SELECT balance FROM Account WHERE number = " + "'" + clicked1.get() + "'"
                    cur.execute(get_curr_bal_2)
                    y = loop(cur.fetchall())
                    new_bal = y+Decimal(INPUT)
                    update_bal ="UPDATE Account SET balance=" + str(new_bal) + " WHERE number = '" + clicked1.get() + "';"
                    cur.execute(update_bal)
                    conn.commit()
                    trans_id = get_trans_id()
                    desc = "'Trasnfered money'"
                    update_transaction_comm = "INSERT INTO Transactions VALUES('Transfer', " + str(INPUT) + ", " + desc + ", " + trans_id + ", " + clicked.get() + ", " + clicked1.get() + ")"
                    print(update_transaction_comm)
                    cur.execute(update_transaction_comm)
                    success_msg.pack()
                    success_msg.place(x=265,y=200)
                    success_msg.config(text="Successfully transfered money!")
                    conn.commit()
                    cur.close()
                    conn.close()
                elif transfer == 'external':
                    ROUTNUM = routing_num.get("1.0", "end-1c")
                    print(ROUTNUM)
                    if ROUTNUM.isdecimal() == False:
                        incor_inp.pack()
                        incor_inp.place(x=200, y=200)
                        incor_inp.config(text='Incorrect Routing Number, please make sure you entered a number')
                    else:
                        conn = psycopg2.connect(user="john",password="password456",host="127.0.0.1",port="5432",database="bank")
                        cur = conn.cursor()
                        get_curr_bal = "SELECT balance FROM Account WHERE number = " + "'" + clicked.get() + "'"
                        cur.execute(get_curr_bal)
                        x = loop(cur.fetchall())
                        newVal = x-Decimal(INPUT)
                        update_val = "UPDATE Account SET balance=" + str(newVal) + " WHERE number = '" + clicked.get() + "';"
                        cur.execute(update_val)
                        conn.commit()
                        trans_id = get_trans_id()
                        desc = "'Trasnfered to external account " + str(ROUTNUM) + "'"
                        update_transaction_comm = "INSERT INTO Transactions VALUES('External Transfer', " + str(INPUT) + ", " + desc + ", " + trans_id + ", " + clicked.get() + ", null" + ")"
                        print(update_transaction_comm)
                        cur.execute(update_transaction_comm)
                        success_msg.pack()
                        success_msg.place(x=275,y=200)
                        success_msg.config(text="Successfully transfered money!")
                        conn.commit()
                        cur.close()
                        conn.close()
                else:
                    print('withdraw/deposite')
                    conn = psycopg2.connect("dbname=bank user=john password=password456")
                    cur = conn.cursor()
                    get_curr_bal = "SELECT balance FROM Account WHERE number = " + "'" + clicked.get() + "'"
                    cur.execute(get_curr_bal)
                    x = loop(cur.fetchall())
                    if transfer == 'withdrawl':
                        newVal = x-Decimal(INPUT)
                    else:
                        newVal = x+Decimal(INPUT)
                    update_val = "UPDATE Account SET balance=" + str(newVal) + " WHERE number = '" + clicked.get() + "';"
                    cur.execute(update_val)
                    conn.commit()
                    trans_id = get_trans_id()
                    desc = "'" + transfer + "'"
                    if transfer == 'deposite':
                        update_transaction_comm = "INSERT INTO Transactions VALUES('" + transfer + "', " + str(INPUT) + ", " + desc + ", " + trans_id + ", " + clicked.get() + ",null)"
                    else:
                        update_transaction_comm = "INSERT INTO Transactions VALUES('" + transfer + "', " + str(INPUT) + ", " + desc + ", " + trans_id + ", null, " + clicked.get() + ")"
                    print(update_transaction_comm)
                    cur.execute(update_transaction_comm)
                    success_msg.pack()
                    success_msg.place(x=265,y=200)
                    if transfer == 'withdrawl':
                        success_msg.config(text="Withdrawl successful!")
                    else:
                        success_msg.config(text='Deopsite Successful!')
                    conn.commit()
                    cur.close()
                    conn.close()
        if loggedInAcc == 'tell':
           acc = self.get_teller_acc()
        else:
            acc = self.get_cust_acc(loggedInAs)
                
        acc = self.get_teller_acc()
        print(acc)
        options = []
        for i in acc:
            for x in i:
                print(x)
                options.append(x)
                    # datatype of menu text
        clicked = tk.StringVar()
            # initial menu text
        clicked.set(options[0])

                    # Create Dropdown menu
        drop = tk.OptionMenu( self , clicked , *options )
        drop.pack()
        drop.place(x=325,y=45)
        confirm_btn = tk.Button(self, text='Confirm', command= lambda: Take_input())
        confirm_btn.pack()
        confirm_btn.place(x=330, y=110)
        amnt_label = tk.Label(self, text='')
        amnt_label.pack()

        inputtxt = tk.Text(self, height = 1,
            width = 10,
            bg = "white",
            fg="red")
        inputtxt.pack()
        inputtxt.place(x=333, y=120)
        if transfer is 'transfer':
            print('in transfer')
            label1 = tk.Label(self, text='Choose account to take money from:')
            label1.pack()
            label1.place(x=270,y=20)
            label2 = tk.Label(self, text='Choose account to transfer to:')
            label2.pack()
            label2.place(x=270,y=70)
            clicked1 = tk.StringVar()

                    # initial menu text
            clicked1.set(options[1])

                    # Create Dropdown menu
            drop1 = tk.OptionMenu( self , clicked1 , *options )
            drop1.pack()
            drop1.place(x=325,y=90)
            confirm_btn.place(x=330,y=160)
            amnt_label.config(text='How much money would you like to transfer? Make sure your input is a number (ex: 50 or 50.00)')
            amnt_label.place(x=70, y=110)
            inputtxt.place(x=333, y=135)
        elif transfer is 'external':
            print('in external')
            label1 = tk.Label(self, text='Choose account to take money from:')
            label1.pack()
            drop.place(x=310, y=45)
            label1.place(x=270,y=20)
            label2 = tk.Label(self, text='Enter routing number of account you would like to send money to')
            label2.pack()
            label2.place(x=200, y=70)
            routing_num = tk.Text(self, height = 1,
            width = 10,
            bg = "white",
            fg="red")
            routing_num.pack()
            routing_num.place(x=333, y=90)
            amnt_label.config(text='How much money would you like to transfer? Make sure your input is a number (ex: 50 or 50.00)')
            amnt_label.place(x=70, y=110)
            inputtxt.place(x=333, y=130)
            confirm_btn.place(x=330, y=150)
        elif transfer in ['networth', 'mean', 'mostvaluable', 'leastvaluable']:
            print('in ' + transfer)

        else:
            print('')
            txt = 'Choose account to ' + transfer + ' from.'
            label1 = tk.Label(self, text=txt)
            label1.pack()
            label1.place(x=270,y=20)
            txt2 = 'How much money would you like to ' + transfer + ' Make sure your input is a number (ex: 50 or 50.00)'
            amnt_label.config(text=txt2)
            amnt_label.place(x=75, y=75)
            inputtxt.place(x=333, y=100)
            confirm_btn.place(x=330, y=125)

        
    def up_frame(self, page_name):
        page = self.listing[page_name]
        page.tkraise()

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        label = tk.Label(self, text = "Login As:")
        label.pack()

        to_employee = tk.Button(self, text = "Employee", command=lambda: controller.up_frame("EmployeePage"))
        to_employee.pack()

        to_customer = tk.Button(self, text = "Customer", command=lambda: controller.up_frame("CustomerLogin"))
        to_customer.pack()


class EmployeePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text = "What kind of employee are you?")
        label.pack()

        to_teller = tk.Button(self, text="Teller", command=lambda: controller.up_frame("TellerLogin"))
        to_teller.pack()

        to_loan = tk.Button(self, text="Loan Specialist")
        to_loan.pack()

        to_manager = tk.Button(self, text="Manager", command=lambda: controller.up_frame("ManagerLogin"))
        to_manager.pack()

        to_login = tk.Button(self, text = "Back to Login Page", command=lambda: controller.up_frame("LoginPage"))
        to_login.pack()

class TellerLogin(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        logged_in_as = ""
        # Hide the dropdown/button and replace with new properties (did this instead of creating a whole new page as this was easier)
        def show():
            drop.pack_forget()
            btn.pack_forget()
            print(clicked.get())
            logged_in_text = "Welcome Back " + clicked.get()
            print(logged_in_text)
            logged_in(logged_in_text, clicked.get())

        # Dropdown menu options
        print('in teller page')            
        options = []
        for i in controller.tellers:
            for x in i:
                print(x)
                options.append(x)
        print(options)

        # datatype of menu text
        clicked = tk.StringVar()

        # initial menu text
        clicked.set(options[0])

        # Create Dropdown menu
        drop = tk.OptionMenu( self , clicked , *options )
        drop.pack()

        # Create button, it will change label text
        btn = tk.Button( self , text = "Login" , command = show )
        btn.pack()

        def logged_in(logged_in_text, loggedInAs):
            #this method is used to "logout", the easiest way I could think to do it was to delete the current tkinter instance and create a new one
            def back():
                label.pack_forget()
                label2.pack_forget()
                btn.pack_forget()
                controller.destroy()
                controller.__init__()
            def to_transaction():
                label2.pack_forget()
                to_transaction_btn.pack_forget()
                choose_transaction(loggedInAs)
            print('in logged in')
            print(logged_in_text)
            label = tk.Label(self, text = logged_in_text)
            label.pack()
            label2 = tk.Label(self, text = "What would you like to do?")
            label2.pack()

            to_transaction_btn = tk.Button(self, text = "Make Transaction", command=to_transaction)
            to_transaction_btn.pack()

            btn= tk.Button(self, text="Logout", command=back)
            btn.pack(side="bottom")
        ###TODO Refactor the bellow functions/pages into main frame so that it can be used by teller and customer
        def choose_transaction(loggedIn):
            def hide_all(transaction):
                label.pack_forget()
                withdraw_btn.pack_forget()
                deposite_btn.pack_forget()
                transfer_btn.pack_forget()
                external_transfer_btn.pack_forget()
                controller.choose_acc(transaction, 'tell', loggedIn)      

            label = tk.Label(self, text='What kind of transaction would you like to make?')
            label.pack()
            
            withdraw_btn = tk.Button(self, text='Make Withdrawl', command=lambda: hide_all('withdraw'))
            withdraw_btn.pack()

            deposite_btn = tk.Button(self, text='Make Deposite', command=lambda: hide_all('deposite'))
            deposite_btn.pack()

            transfer_btn = tk.Button(self, text='Transfer', command=lambda: hide_all('transfer'))
            transfer_btn.pack()

            external_transfer_btn = tk.Button(self, text='External Transfer', command=lambda: hide_all('external'))
            external_transfer_btn.pack()

class CustomerLogin(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        logged_in_as = ""
        # Hide the dropdown/button and replace with new properties (did this instead of creating a whole new page as this was easier)
        def show():
            drop.pack_forget()
            btn.pack_forget()
            print(clicked.get())
            logged_in_text = "Welcome Back " + clicked.get()
            print(logged_in_text)
            logged_in(logged_in_text, clicked.get())

        # Dropdown menu options
        print('in cust page')            
        options = []
        for i in controller.customers:
            for x in i:
                print(x)
                options.append(x)
        print(options)

        # datatype of menu text
        clicked = tk.StringVar()

        # initial menu text
        clicked.set(options[0])

        # Create Dropdown menu
        drop = tk.OptionMenu( self , clicked , *options )
        drop.pack()

        # Create button, it will change label text
        btn = tk.Button( self , text = "Login" , command = show )
        btn.pack()

        def logged_in(logged_in_text, loggedInAS):
            #this method is used to "logout", the easiest way I could think to do it was to delete the current tkinter instance and create a new one
            def back():
                label.pack_forget()
                label2.pack_forget()
                btn.pack_forget()
                controller.destroy()
                controller.__init__()
            def to_transaction():
                label2.pack_forget()
                to_transaction_btn.pack_forget()
                choose_transaction(loggedInAS)
            print('in logged in')
            print(logged_in_text)
            label = tk.Label(self, text = logged_in_text)
            label.pack()
            label2 = tk.Label(self, text = "What would you like to do?")
            label2.pack()

            to_transaction_btn = tk.Button(self, text = "Make Transaction", command=to_transaction)
            to_transaction_btn.pack()

            btn= tk.Button(self, text="Logout", command=back)
            btn.pack(side="bottom")
        ###TODO Refactor the bellow functions/pages into main frame so that it can be used by teller and customer
        def choose_transaction(loggedIn):
            def hide_all(transaction):
                label.pack_forget()
                withdraw_btn.pack_forget()
                deposite_btn.pack_forget()
                transfer_btn.pack_forget()
                external_transfer_btn.pack_forget()
                controller.choose_acc(transaction, 'cust', loggedIn)      

            label = tk.Label(self, text='What kind of transaction would you like to make?')
            label.pack()
            
            withdraw_btn = tk.Button(self, text='Make Withdrawl', command=lambda: hide_all('withdraw'))
            withdraw_btn.pack()

            deposite_btn = tk.Button(self, text='Make Deposite', command=lambda: hide_all('deposite'))
            deposite_btn.pack()

            transfer_btn = tk.Button(self, text='Transfer', command=lambda: hide_all('transfer'))
            transfer_btn.pack()

            external_transfer_btn = tk.Button(self, text='External Transfer', command=lambda: hide_all('external'))
            external_transfer_btn.pack()
            
class ManagerLogin(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        logged_in_as = ""
        # Hide the dropdown/button and replace with new properties (did this instead of creating a whole new page as this was easier)
        def show():
            drop.pack_forget()
            btn.pack_forget()
            print(clicked.get())
            logged_in_text = "Welcome Back " + clicked.get()
            print(logged_in_text)
            logged_in(logged_in_text)

        # Dropdown menu options
        print('in manager page')            
        options = []
        for i in controller.managers:
            for x in i:
                print(x)
                options.append(x)
        print(options)

        # datatype of menu text
        clicked = tk.StringVar()

        # initial menu text
        clicked.set(options[0])

        # Create Dropdown menu
        drop = tk.OptionMenu( self , clicked , *options )
        drop.pack()

        # Create button, it will change label text
        btn = tk.Button( self , text = "Login" , command = show )
        btn.pack()

        def logged_in(logged_in_text):
            #this method is used to "logout", the easiest way I could think to do it was to delete the current tkinter instance and create a new one
            def back():
                label.pack_forget()
                label2.pack_forget()
                btn.pack_forget()
                controller.destroy()
                controller.__init__()
            def to_analytics():
                label2.pack_forget()
                to_transaction_btn.pack_forget()
                choose_analytics()
            def to_acc_man():
                label2.pack_forget()
                acc_man_btn.pack_forget()
                to_transaction_btn.pack_forget()
                choose_acc_man()
            print('in logged in')
            print(logged_in_text)
            label = tk.Label(self, text = logged_in_text)
            label.pack()
            label2 = tk.Label(self, text = "What would you like to do?")
            label2.pack()

            acc_man_btn = tk.Button(self, text = 'Account Management', command=to_acc_man)
            acc_man_btn.pack()

            to_transaction_btn = tk.Button(self, text = "Analytics", command=to_analytics)
            to_transaction_btn.pack()
            
            btn= tk.Button(self, text="Logout", command=back)
            btn.pack(side="bottom")
        def choose_acc_man():
            def acc_man_exec(action):
                label.pack_forget()
                create_btn.pack_forget()
                delete_btn.pack_forget()
                controller.manager_acc_man(action)
            label = tk.Label(self, text='Which action would you like to take?')
            label.pack()

            create_btn = tk.Button(self, text = 'Create account', command=lambda: acc_man_exec('create'))
            create_btn.pack()

            delete_btn = tk.Button(self, text = 'Delete account', command=lambda: acc_man_exec('delete'))
            delete_btn.pack()
        def choose_analytics():
            def analyt(analytic):
                label.pack_forget()
                networth_btn.pack_forget()
                mean_btn.pack_forget()
                mostvaluable_btn.pack_forget()
                leastvaluable_btn.pack_forget()
                controller.choose_ana(analytic)      

            label = tk.Label(self, text='What kind of data would you like to view?')
            label.pack()
            
            networth_btn = tk.Button(self, text='Total net worth of all customers', command=lambda: analyt('networth'))
            networth_btn.pack()

            mean_btn = tk.Button(self, text='Mean balance for all customers', command=lambda: analyt('mean'))
            mean_btn.pack()

            mostvaluable_btn = tk.Button(self, text='Most valuable account', command=lambda: analyt('mostvaluable'))
            mostvaluable_btn.pack()
            
            leastvaluable_btn = tk.Button(self, text='Least valuable account', command=lambda: analyt('leastvaluable'))
            leastvaluable_btn.pack()




if __name__ == '__main__':
    app = MainFrame()
    app.mainloop()