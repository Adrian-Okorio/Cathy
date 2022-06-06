import hashlib
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

plt.rcParams.update({'figure.figsize': (6, 4), 'figure.dpi': 80})


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


def view_available_computers():
    c.execute('SELECT * FROM computerstable where Status = "Available"')
    data = c.fetchall()
    return data


def add_computer(ComputerNo, Brand, Status):
    c.execute('INSERT INTO computerstable(ComputerNo, Brand, Status) VALUES (?,?,?)',
              (ComputerNo, Brand, Status))
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


def book_computer(Status, Status1):
    c.execute("update computerstable set Status= ? where Status = ? ", (Status, Status1))
    conn.commit()
    data = c.fetchall()
    return data


def delete_computer(computer):
    c.execute('DELETE FROM computerstable WHERE computerNo="{}"'.format(computer))
    conn.commit()


# Students database management
def create_usertable():
    c.execute(
        'CREATE TABLE IF NOT EXISTS userstable(StudentNo TEXT, FirstName TEXT, LastName TEXT,Email TEXT,Phone ,'
        'Password TEXT)')


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


def delete_student(users):
    c.execute('DELETE FROM userstable WHERE StudentNo="{}"'.format(users))
    conn.commit()


def main():
    col1, col2, col3 = st.columns(3)
    with col2:
        st.image("https://raw.githubusercontent.com/project152/Cathy/main/loggo.jpg")

    st.markdown("<h1 style='text-align: center; color:#464e5f;'>Computer Laboratory Management System</h1>",
                unsafe_allow_html=True)

    menu = ["Home", "Admin Login", "Students Login", "SignUp"]
    choice = st.sidebar.selectbox("Makerere University Computer Laboratory "
                                  " Management Sytem", menu, disabled=False)

    if choice == "Home":
        st.write("""# Home""")

        st.write("""### Welcome to the Makerere University Online Management System""")
        st.write("""The Makerere University Online Management System is a web based system that is used to 
         manage, monitor and control computer usage within the laboratory""")
        st.write("""#### Please note that A valid university id is required upon entrance""")
        st.write("Below is a list of all the computers and there current status, Students can only Book a computer "
                 "that is with satus 'Available'")
        col4, col5 =st.columns(2)
        with col4:
            computer_result = view_all_computers()
            clean_db = pd.DataFrame(computer_result, columns=["Computer_Number", "Type", "Availability"])
            st.dataframe(clean_db)
            st.write("'Out of Service' stands for all computes that are currently under repair, malfunctioned "
                     "or going though updates")

        with col5:
            st.write('Summary of the computer laboratory Activities')
            c.execute('SELECT * FROM computerstable')
            data3 = c.fetchall()
            data4 = pd.DataFrame(data3, columns=['Computer_Number', 'Brand', 'Status'])
            sammary = data4['Status'].value_counts().to_frame()
            sammary = sammary.reset_index()
            st.dataframe(sammary)


            st.write("'Available' stands for all computes that are currently free")
            st.write("'In Use' stands for all computes that are currently occupied by a Student")
            st.write("'Booked' stands for all computes that have been secured though the online sytem however "
                     "if a  student takes more than three hours to arrive to the the computer laboratory, "
                     "the computer will be marked available for anyone to use")



        st.write("""##### Note: all students should login to be able book a computer if available""")





    elif choice == "Admin Login":
        st.sidebar.warning("To test functionality of the Administration account the "
                           "User Name has been set to 'Admin', and password to 'admin'")

        st.subheader("Login Section")
        username = st.sidebar.text_input("User Name -> Admin ")
        password = st.sidebar.text_input("Password -> admin ", type='password')
        if st.sidebar.checkbox("Login"):
            if (password == 'admin') & (username == 'Admin'):
                st.success("You have successfully Logged in as Administrator")

                with st.expander("View all student records"):
                    c.execute('SELECT * FROM userstable')
                    data = c.fetchall()
                    data1 = pd.DataFrame(data
                                         , columns=["StudentNo", "FirstName", "LastName", "Email", "Phone", "Password"])
                    data2 = st.dataframe(data1)
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
                    # st.write(computer_result)

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

                    print(view_all_users())
                    list_of_users = [i[0] for i in view_all_users()]
                    selected_user = st.selectbox("Please select the computer to Delete", list_of_users)
                    st.warning("Do you want to delete user {} ? ".format(selected_user))
                    if st.button("Delete Student"):
                        delete_student(selected_user)
                        st.success("{} Student record has been Deleted ".format(selected_user))

                with st.expander("Delete Computer record"):
                    st.write('Current Data')
                    c.execute('SELECT * FROM computerstable')
                    data31 = c.fetchall()
                    data41 = pd.DataFrame(data31, columns=['Computer_Number', 'Brand', 'Status'])
                    data51 = st.dataframe(data41)
                    print(data51)

                    print(view_all_computer_numbers())
                    list_of_computers = [i[0] for i in view_all_computer_numbers()]
                    selected_computer = st.selectbox("Please select the computer to Delete", list_of_computers)
                    st.warning("Do you want to delete computer {} ? ".format(selected_computer))
                    if st.button("Delete Computer"):
                        delete_computer(selected_computer)
                        # edit_computer_data(new_computer, new_Brand, new_Status, Computer_Number, Brand, Status)
                        st.success("{} Computer has been Deleted ".format(selected_computer))

                    st.write('Updated Data')
                    computer_result1 = view_all_computers()
                    clean_db1 = pd.DataFrame(computer_result1, columns=["Computer_Number", "Type", "Availability"])
                    st.dataframe(clean_db1)

                with st.expander("Summary statistics"):
                    st.write('Summary of the comp lab')
                    sammary = data4['Brand'].value_counts().to_frame()
                    sammary = sammary.reset_index()
                    st.dataframe(sammary)

                with st.expander("Add New Computer"):
                    st.write("Add New Computer")

                    col13, col23 = st.columns(2)

                    with col13:
                        ComputerNo = st.text_area("Computer_Number")

                    with col23:
                        Brand = st.text_input("Brand")
                        Status = st.selectbox("Status", ["Available", "Booked", "In Use", "Out of Service"])
                        # new_Status = st.text_input("Status", Status)

                    if st.button("Add Computer"):
                        add_computer(ComputerNo, Brand, Status)
                        st.success("{} Computer Numbed {} has been Added ".format(Brand, ComputerNo))

                        st.write("Updated Computer Data")
                        c.execute('SELECT * FROM computerstable')
                        data3 = c.fetchall()
                        data4 = pd.DataFrame(data3, columns=['Computer_Number', 'Brand', 'Status'])
                        data5 = st.dataframe(data4)
                        print(data5)

            else:
                st.warning("Incorrect Username/Password")

            st.write("Click Home to automatically log out")



    elif choice == "Students Login":
        st.subheader("Login Section")

        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type='password')
        if st.sidebar.checkbox("Login"):
            create_usertable()
            hashed_pswd = make_hashes(password)

            result = login_user(username, check_hashes(password, hashed_pswd))
            if result:

                with st.expander("View avaliable computers"):
                    st.success("Logged In as {}".format(username))
                    c.execute("SELECT * FROM computerstable WHERE Status ='Availiable' ")
                    datav = c.fetchall()
                    datab = pd.DataFrame(datav, columns=['Computer_Number', 'Brand', 'Status'])
                    datan = st.dataframe(datab)
                    print(datan)


                task = st.selectbox("Task", ["Book computer", "Cancel booked Computer", ])
                if task == "Book computer":
                    st.subheader("Book computer")

                    print(view_available_computers())
                    list_of_computers = [i[0] for i in view_available_computers()]
                    selected_computer = st.selectbox("Please select the computer to Book", list_of_computers)
                    computer_result = get_computer(selected_computer)


                    if computer_result:
                        Computer_Number = computer_result[0][0]
                        Brand = computer_result[0][1]
                        Status = computer_result[0][2]

                        col1, col2 = st.columns(2)

                        with col1:
                            new_computer = st.write("Computer_Number", Computer_Number)
                            new_Brand = st.write("Brand", Brand)
                            new_Status = st.selectbox(Status, ["Available", "Booked"])


                        if st.button("Book Computer"):
                            edit_computer_data(Computer_Number, Brand, new_Status, Computer_Number, Brand, Status)
                            st.success("You Successfully booked Computer {}  ".format(Computer_Number))

                            st.write("Updated Computer Data")
                            c.execute('SELECT * FROM computerstable')
                            data3 = c.fetchall()
                            data4 = pd.DataFrame(data3, columns=['Computer_Number', 'Brand', 'Status'])
                            data5 = st.dataframe(data4)
                            print(data5)

            else:
                st.warning("Incorrect Username/Password")







    elif choice == "SignUp":
        st.subheader("Create New Account")

        new_StudentNo = st.text_input("StudentNo ( Note: using a student number that already exists int the system "
                                      "will lead "
                                      "to error)")
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
