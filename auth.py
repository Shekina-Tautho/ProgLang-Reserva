import csv
from pathlib import Path

filename = "users.csv"
filepath = 'files/users.csv'
path = Path(filepath)

fields = []
rows = []
role = "user"
found = False

uname = ""
pword = ""


def create_csv():
    csv_file_path = 'files/users.csv'
    
    with open(csv_file_path, 'w', newline='') as file:
        data = [['username', 'password', 'role']]
        writer = csv.writer(file)
        writer.writerows(data)


def load_csv():
     with open(filepath, 'r') as csvfile:
         csvreader = csv.reader(csvfile)
         
         fields = next(csvreader)
         for row in csvreader:
             rows.append(row)
     return rows

def add_record():
    data = [[uname, pword, role]]
    with open(filepath, 'a', newline='') as file:
       writer = csv.writer(file)
       writer.writerows(data)
           
    
def login():
    print("Welcome to the login page!")
    username = input("Please enter your username: ")
    password = input("Please enter your password: ")
    
    global found
    found = False
    if path.exists():
        global rows
        rows = []
        load_csv()
        for row in rows:
            if (row[0] == username) and (row[1] == password):
                found = True
                break
            
        if found:
            print("Successfully logged in.")
        else:
            print("Login attempt unsuccessful.")
    else:
        create_csv()
            

    
def register():
    print("Welcome to the register page!")
    username = input("Please enter the username you want to use: ")
    password = input("Please enter the password you want to use: ")
    
    global found 
    found = False
    if path.exists():
        global rows
        rows = []
        load_csv()
        for row in rows:
            if (row[0] == username):
                found = True
                break
        
        if found:
            print("An account with this username already exists.")
        else:
            global uname, pword
            uname = username
            pword = password
            add_record()
            
    else:
        create_csv()