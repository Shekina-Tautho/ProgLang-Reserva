import csv

filename = "users.csv"
filepath = 'files/users.csv'

fields = []
rows = []
role = "user"
found = False


def create_csv():
    data = ['username', 'password', 'role']
    csv_file_path = 'files/users.csv'
    
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)


def load_csv():
     with open(filepath, 'r') as csvfile:
         csvreader = csv.reader(csvfile)
         
         fields = next(csvreader)
         for row in csvreader:
             rows.append(row)
     return rows
    
          
    
def login():
    print("Welcome to the login page!")
    username = input("Please enter your username: ")
    password = input("Please enter your password: ")
    load_csv()
    for row in rows:
        if (row[0] == username) and (row[1] == password):
            global found
            found = True
            break
        
    if found:
        print("Successfully logged in.")
    else:
        print("Login attempt unsuccessful.")
            

    
    
def register():
    print("Welcome to the register page!")
    username = input("Please enter the username you want to use: ")
    password = input("Please enter the password you want to use: ")
    