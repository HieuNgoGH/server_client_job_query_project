import tkinter as tk
from tkinter import ttk, END, Text
import requests
import json
import zmq
import os


LARGEFONT = ("Verdana", 35)

class tkinterApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.query = None
        self.frames = {}

        for F in (homePage, helpPage, resultsPage, detailsPage, signUpPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(homePage)

    def get_query_results(self):
        return self.query

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


    def get_listings(self, query):

        os.system('cls')
        context = zmq.Context()

        # socket to talk to server

        print("connecting to remote jobs server")
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://localhost:5555")

        variable = query

        # do something
        #socket.send_string(variable)
        socket.send(json.dumps(variable).encode("utf-8"))
        print("Sent request for" + " " + variable)

        #message = socket.recv
        message = json.loads(socket.recv().decode('utf-8'))
        print('Waiting for respsonse.')
        print('Reponse received.')

        for item in message["data"]:
            print(item["employer_name"])
            print(item["job_title"])
            print(item["job_description"])
            print(item["job_city"])
            print(item["job_state"])


class homePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        jt = tk.StringVar()
        city = tk.StringVar()

        label = ttk.Label(self, text="Remote Me Jobs", font=LARGEFONT)
        label.grid(row=0, column=3, padx=200, pady=10)

        job_title_lable = ttk.Label(self, text="Enter job title:", font="bold")
        job_title_lable.grid(row=1, column=2, padx=0, pady=0)
        job_title_entry = ttk.Combobox(self, width=27, textvariable=jt, values=['Python Developer', 'Computer Engineer','Web Developer', 'Sales', 'IT Specialist', 'Data Scientist'])
        job_title_entry.grid(row=1, column=3, padx=0, pady=0)

        enter_city = ttk.Label(self, text="Enter city", font="bold")
        enter_city.grid(row=2, column=2, padx=0, pady=0)
        enter_city_entry = ttk.Entry(self, textvariable=city)
        enter_city_entry.grid(row=2, column=3, padx=0, pady=0)


        resultsPageButton = ttk.Button(self, text="Submit", command=lambda:[tkinterApp.get_listings(self, jt.get()),
        controller.show_frame(resultsPage)])
        resultsPageButton.grid(row=5, column=8, padx=10, pady=10)

        signUpButton = ttk.Button(self, text="Sign Up", command=lambda:controller.show_frame(signUpPage))
        signUpButton.grid(row=5, column=2, padx=10, pady=10)



class resultsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text="Remote Me Jobs - Search Results", font=LARGEFONT)
        label.grid(row=0, column=1)
        #label.grid(row=0, column=2, padx=10, pady=10)

        employer_name = ttk.Label(self, text="Employer Name")
        employer_name.grid(row=1, column=0)

        job_title = ttk.Label(self, text="Job Title")
        job_title.grid(row=1, column=1)

        job_location = ttk.Label(self, text="Job Location")
        job_location.grid(row=1, column=2)


        backbutton = ttk.Button(self, text="Back", command=lambda:controller.show_frame(homePage))
        backbutton.grid(row=5, column=0, padx=1, pady=100)

        helpbutton = ttk.Button(self, text="Help", command=lambda:controller.show_frame(helpPage))
        helpbutton.grid(row=5, column=3, padx=1, pady=100)

class helpPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Help Page", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        various_help_topics = tk.Label(self, text="Various help topics here")
        various_help_topics.grid(row=1, column=2, padx=40)

        email_us = ttk.Label(self, text="If you have any further questions email us at: help_me@jobs.com")
        email_us.grid(row=2, column=2, padx=40)

        backbutton = ttk.Button(self, text="Back", command=lambda:controller.show_frame(resultsPage))
        backbutton.grid(row=1, column=1, padx=10, pady=10)

class detailsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Job Details", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        backbutton = ttk.Button(self, text="Back", command=lambda:controller.show_frame(resultsPage))
        backbutton.grid(row=1, column=1, padx=10, pady=10)

class signUpPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Sign Up Page", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        fn = tk.StringVar()
        ln = tk.StringVar()
        email = tk.StringVar()

        enter_first_name = ttk.Label(self, text="Enter First Name:")
        enter_first_name.grid(row=1, column=3, padx=10)
        enter_first_name_entry = ttk.Entry(self, textvariable=fn)
        enter_first_name_entry.grid(row=1, column=4, padx=10)

        enter_last_name = ttk.Label(self, text="Enter Last Name:")
        enter_last_name.grid(row=2, column=3, padx=10)
        enter_last_name_entry = tk.Entry(self, textvariable=ln)
        enter_last_name_entry.grid(row=2, column=4, padx=10)

        enter_email = ttk.Label(self, text="Please enter email address:")
        enter_email.grid(row=3, column=3, padx=10)
        email_entry = tk.Entry(self, textvariable=email)
        email_entry.grid(row=3, column=4, padx=10)


        backbutton = ttk.Button(self, text="Back", command=lambda:controller.show_frame(homePage))
        backbutton.grid(row=5, column=3, padx=10, pady=10)

        submit_button = ttk.Button(self, text="Submit", command=lambda:controller.show_frame(homePage))
        submit_button.grid(row=5, column=4, padx=10, pady=10)

app = tkinterApp()
app.mainloop()
