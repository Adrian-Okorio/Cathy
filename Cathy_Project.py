import pandas as pd
import streamlit as st



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
    c.execute('CREATE TABLE IF NOT EXISTS computerstable(Computer_Number TEXT,Availability TEXT,Booked BOOLEAN)')


def view_all_computers():
    c.execute('SELECT * FROM computerstable')
    data = c.fetchall()
    return data


def add_computerdata(computer_number, Availability, booked):
    # c.execute('INSERT INTO computerstable(Computer_Number TEXT,Availability TEXT,Booked BOOLEAN) VALUES (?,?)'),(Computer_Number, Availability, Booked))
    conn.commit()


# Students database management
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username, password):
    c.execute('INSERT INTO userstable(username,password) VALUES (?,?)', (username, password))
    conn.commit()


def login_user(username, password):
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?', (username, password))
    data = c.fetchall()
    return data


def view_all_users():
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data


def main():
    st.title("Computer Laboratory Management System")

    menu = ["Home", "Admin Login", "Students Login", "SignUp"]
    choice = st.sidebar.selectbox("Makerere University Computer Laboratory "
                                  " Management Sytem", menu, disabled=False)

    if choice == "Home":
        st.subheader("Home")
        st.write("""description of  what the comp lab is  """)
        ##show avaiable computers

        with st.expander("Check for Avaliable computers"):
            st.write("""This is a list showing computers that are available for use""")
            st.write("""Please note that A valid university id is required upon entrance""")
            computer_result = view_all_computers()
            clean_db = pd.DataFrame(computer_result, columns=["Username", "Password", "Booked"])
            st.dataframe(clean_db)

        st.write("""Note: all students should log in to be able book a computer if available""")













    elif choice == "Admin Login":
        st.subheader("Login Section")
        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type='password')
        if st.sidebar.checkbox("Login"):
            create_usertable()
            hashed_pswd = make_hashes(password)

            result = login_user(username, check_hashes(password, hashed_pswd))
            if result:
                st.success("You have successfully Logged in as Administrator")

                create_computerstable()
                # add_computerdata(Computer_Number,Availability,Booked)

                # state availability of a computer or not ( under maintainable)
                with st.expander("View all Registered students"):
                    user_result = view_all_computers()
                    clean_db = pd.DataFrame(user_result, columns=["Computer Number", "Available", "booked"])
                    st.dataframe(clean_db)

                with st.expander("Add new Computer"):
                    st.write('Add new computer')

                with st.expander("Edit computer Availability"):
                    st.write('Edit computers')





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
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type='password')

        if st.button("Signup"):
            create_usertable()
            add_userdata(new_user, make_hashes(new_password))
            st.success("You have successfully created a valid Account")
            st.info("Go to Login Menu to login")


if __name__ == '__main__':
    main()
