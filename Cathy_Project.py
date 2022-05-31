


import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
#import plotly.express as px
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

plt.rcParams.update({'figure.figsize': (6, 4), 'figure.dpi': 80})

# Security
# passlib,hashlib,bcrypt,scrypt
import hashlib


def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()


def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False

# DB Management
import sqlite3

conn = sqlite3.connect('Comp_lab_data.db')
c = conn.cursor()


# DataBase Management  Functions
# Admin database management
def create_computerstable():
    c.execute('CREATE TABLE IF NOT EXISTS computerstable(ComputerNo TEXT,Type TEXT,Status TEXT)')


def view_all_computers():
    c.execute('SELECT * FROM computerstable')
    data = c.fetchall()
    return data


def add_computerdata(computer_number, Availability, booked):
    # c.execute('INSERT INTO computerstable(Computer_Number TEXT,Availability TEXT,Booked BOOLEAN) VALUES (?,?)'),(Computer_Number, Availability, Booked))
    conn.commit()


def view_all_computer_numbers():
    c.execute('SELECT DISTINCT ComputerNo FROM computerstable')
    data = c.fetchall()
    return data


def get_computer(computer):
    c.execute('SELECT * FROM computerstable WHERE computerNo="{}"'.format(computer))
    data = c.fetchall()
    return data


def edit_computer_data(new_computer, new_Brand, new_Status, ComputerNo, Brand, Status):
    c.execute(
        "UPDATE computerstable SET ComputerNo =?,Brand=?,Status=? WHERE ComputerNo=? and Brand=? and Status=? ",
        (new_computer, new_Brand, new_Status, ComputerNo, Brand, Status))
    conn.commit()
    data = c.fetchall()
    return data


# Students database management
def create_usertable():
    c.execute(
        'CREATE TABLE IF NOT EXISTS userstable(StudentNo TEXT, FirstName TEXT, LastName TEXT,Email TEXT,Phone ,Password TEXT)')


def add_userdata(StudentNo, FirstName, LastName, Email, Phone, Password):
    c.execute('INSERT INTO userstable(StudentNo, FirstName, LastName, Email, Phone, Password) VALUES (?,?,?,?,?,?)',
              (StudentNo, FirstName, LastName, Email, Phone, Password))
    conn.commit()


def login_user(StudentNo, password):
    c.execute('SELECT * FROM userstable WHERE StudentNo =? AND password = ?', (StudentNo, password))
    data = c.fetchall()
    return data


def view_all_users():
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data


def main():
    col1, col2, col3 = st.columns(3)
    with col2:
        st.image("https://raw.githubusercontent.com/project152/Cathy/main/loggo.jpg")

    st.markdown("<h1 style='text-align: center; color: black;'>Computer Laboratory Management System</h1>",
                unsafe_allow_html=True)

    menu = ["Home", "Admin Login", "Students Login", "SignUp"]
    choice = st.sidebar.selectbox("Makerere University Computer Laboratory "
                                  " Management Sytem", menu, disabled=False)

    if choice == "Home":
        st.subheader("Home")
        st.write("""description of  what the comp lab is  """)
        ##show avaiable computers

        st.write("""This is a list showing computers that are available for use""")
        st.write("""Please note that A valid university id is required upon entrance""")
        computer_result = view_all_computers()
        clean_db = pd.DataFrame(computer_result, columns=["Computer_Number", "Type", "Availability"])
        st.dataframe(clean_db)

        st.write("""Note: all students should log in to be able book a computer if available""")



    elif choice == "Admin Login":
        st.subheader("Login Section")
        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type='password')
        if st.sidebar.checkbox("Login"):
            if (password == 'admin') & (username == 'Admin'):
                st.success("You have successfully Logged in as Administrator")
                # create_usertable()
                # hashed_pswd = make_hashes(password)

                # result = login_user(username, check_hashes(password, hashed_pswd))
                # if result:
                # st.success("You have successfully Logged in as Administrator")

                # create_computerstable()
                # add_computerdata(Computer_Number,Availability,Booked)

                # state availability of a computer or not ( under maintainable)
                c.execute('SELECT * FROM userstable')
                data = c.fetchall()
                data1 = pd.DataFrame(data, columns=["StudentNo", "FirstName", "LastName", "Email", "Phone", "Password"])
                data2 = st.dataframe(data1)
                with st.expander("View all Registered students"):
                    print(data2)

                with st.expander("View all Computer"):
                    st.write('Available computer')
                    c.execute('SELECT * FROM computerstable')
                    data3 = c.fetchall()
                    data4 = pd.DataFrame(data3, columns=['Computer_Number', 'Brand', 'Status'])
                    data5 = st.dataframe(data4)
                    print(data5)

                with st.expander("Update computer Status"):
                    st.write('Current Data')
                    computer_status = st.selectbox("Status",
                                                   ["Available", "In use", "Under maintainace", "Not Avaliable "])
                    c.execute('SELECT * FROM computerstable')
                    data3 = c.fetchall()
                    data4 = pd.DataFrame(data3, columns=['Computer_Number', 'Brand', 'Status'])
                    data5 = st.dataframe(data4)
                    print(data5)

                    # getting unique computers
                    print(view_all_computer_numbers())
                    list_of_computers = [i[0] for i in view_all_computer_numbers()]
                    selected_computer = st.selectbox("Please select the computer to update", list_of_computers)
                    computer_result = get_computer(selected_computer)
                    #st.write(computer_result)

                    if computer_result:
                        Computer_Number = computer_result[0][0]
                        Brand = computer_result[0][1]
                        Status = computer_result[0][2]

                        col1, col2 = st.columns(2)

                        with col1:
                            new_computer = st.text_area("Computer_Number", Computer_Number)

                        with col2:
                            new_Brand = st.text_input("Brand", Brand)
                            new_Status = st.selectbox(Status, ["Available", "Booked", "In Use", "Out of Service"])
                            # new_Status = st.text_input("Status", Status)

                        if st.button("Update Computer"):
                            edit_computer_data(new_computer, new_Brand, new_Status, Computer_Number, Brand, Status)
                            st.success("{} Computer has been Updated ".format(Computer_Number))

                    st.write("Updated Computer Data")
                    c.execute('SELECT * FROM computerstable')
                    data3 = c.fetchall()
                    data4 = pd.DataFrame(data3, columns=['Computer_Number', 'Brand', 'Status'])
                    data5 = st.dataframe(data4)
                    print(data5)

                with st.expander("Delete Student record"):
                    st.write('update computers')

                with st.expander("Delete Computer record"):
                    st.write('update computers')

                with st.expander("Summary statistics"):
                    st.write('Summary of the comp lab')
                    sammary = data4['Brand'].value_counts().to_frame()
                    sammary = sammary.reset_index()
                    st.dataframe(sammary)

                 #   p1 = px.pie(sammary, names='index', values='Brand')
                  #  st.plotly_chart(p1, use_container_width=True)



            else:
                st.warning("Incorrect Username/Password")


    elif choice == "Students Login":
        st.subheader("Login Section")

        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type='password')
        if st.sidebar.checkbox("Login"):
            create_usertable()
            hashed_pswd = make_hashes(password)

            result = login_user(username, check_hashes(password, hashed_pswd))
            if result:

                st.success("Logged In as {}".format(username))

                task = st.selectbox("Task", ["Book computer", "Cancel booked Computer", ])
                if task == "Add Post":
                    st.subheader("Book computer")

                elif task == "Analytics":
                    st.subheader("Cancel booked Computer")
                    c.execute('SELECT * FROM computerstable')
                    data = c.fetchall()
                    data1 = pd.DataFrame(data, columns=["Username", "Password", "Booked"])
                    data2 = st.dataframe(data1)
                    print(data2)

            #    elif task == "Profiles":
            #        st.subheader("User Profiles")
            #        user_result = view_all_users()
            #        clean_db = pd.DataFrame(user_result, columns=["Username", "Password"])
            #        st.dataframe(clean_db)
            else:
                st.warning("Incorrect Username/Password")





    elif choice == "SignUp":
        st.subheader("Create New Account")

        new_StudentNo = st.text_input("StudentNo")
        new_FirstName = st.text_input("FirstName")
        new_LastName = st.text_input("LastName")
        new_email = st.text_input("Email")
        new_phone = st.text_input("Phone")
        new_password = st.text_input("Password", type='password')

        if st.button("Signup"):
            create_usertable()
            add_userdata(new_StudentNo, new_FirstName, new_LastName, new_email, new_phone, make_hashes(new_password))
            st.success("You have successfully created a valid Account")
            st.info("Go to Login Menu to login")


if __name__ == '__main__':
    main()
