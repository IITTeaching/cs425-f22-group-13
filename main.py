import tkinter as tk
#import psycopg2

class MainFrame(tk.Tk):
    #Frame object holding all pages
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("750x350")

        container = tk.Frame(self)
        container.pack(fill='both', expand=1)

        self.listing = {}

        for p in (LoginPage, EmployeePage) :
            page_name = p.__name__
            frame = p(parent = container, controller = self)
            frame.place(relheight=1, relwidth=1)
            self.listing[page_name] = frame
        self.up_frame('LoginPage')
        
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

        to_customer = tk.Button(self, text = "Customer")
        to_customer.pack()


class EmployeePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text = "What kind of employee are you?")
        label.pack()

        to_teller = tk.Button(self, text="Teller")
        to_teller.pack()

        to_loan = tk.Button(self, text="Loan Specialist")
        to_loan.pack()

        to_manager = tk.Button(self, text="Manager")
        to_manager.pack()

        to_login = tk.Button(self, text = "Back to Login Page", command=lambda: controller.up_frame("LoginPage"))
        to_login.pack()

if __name__ == '__main__':
    app = MainFrame()
    app.mainloop()