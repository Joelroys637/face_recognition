import streamlit as st
import sqlite3
from streamlit_option_menu import option_menu
import main1 as fac
import streamlit_custome_css as leo










selected = option_menu(
    menu_title="",
    options=["login","sigup"],
    icons=["box-arrow-in-right","person-plus"],
    orientation="horizontal",
)
if selected=="login":
    st.session_state["page"] = "login"
else:
    st.session_state["page"] = "signup"


leo.header_hide()
# Database setup
conn = sqlite3.connect('login_face.db')
c = conn.cursor()

# Create users table
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    name TEXT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    email TEXT NOT NULL
)
''')
conn.commit()


def register_user(name, username, password, email):
    try:
        c.execute('INSERT INTO users (name, username, password, email) VALUES (?, ?, ?, ?)',(name, username, password, email))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False


def validate_user(username, password):
    c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    return c.fetchone()


# Initialize session state
if "page" not in st.session_state:
    st.session_state["page"] = "signup"  # Default to signup page
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False  # User is not logged in initially
if "username" not in st.session_state:
    st.session_state["username"] = None  # Store logged-in username


# Main page content (after login)

    


# Login and signup pages
def login_page():
    
    st.markdown("""
    <style>
    .stMain {
        background-image: url('https://stoutonia.com/wp-content/uploads/2018/05/beach-blur-boardwalk-132037-900x600.jpg'); /* Local background image */
        background-size: cover;
    }
    
    .login-button {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 20px;
    }
    .login-form {
        background-color: rgba(0, 0, 0, 0.6);  /* Semi-transparent black */
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        width: 100%;
        max-width: 400px;
    }
    h2 {
        color: #fff;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown('''<center><h2 id="login" style="color: white;">Staff Login</h2></center>''', unsafe_allow_html=True)
    
    username = st.text_input("Username", placeholder="Enter Username")
    password = st.text_input("Password", type="password", placeholder="Enter Password")
    # Add custom CSS to style the form and page
    st.markdown("""
        <style>
        .stApp {
            background-image: url('');
            background-size: cover;
            background-position: center;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .login-form {
            background-color: rgba(0, 0, 0, 0.6);  /* Semi-transparent black */
            padding: 30px;
            border-radius: 10px;
            text-align: center;
            width: 100%;
            max-width: 400px;
        }

        .stForm {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }

        .stButton button {
            display: block;
            width: 50%;  /* Make button width smaller and center */
            margin-top: 20px;  /* Space above the button */
            margin-left: auto;
            margin-right: auto;
        }

        h2 {
            color: white;
            margin-bottom: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Create the form for login
    with st.form(key='login_form'):
        

        # Username and password fields
        
        
        # Login button inside the form
        submit_button = st.form_submit_button("Login")
    st.markdown(
    """
    <style>
    .link-button {
        background: none;
        border: none;
        color: blue;
        text-decoration: underline;
        cursor: pointer;
        font-size: 16px;
    }
    .link-button:hover {
        color: darkblue;
    }
    </style>
    """,
    unsafe_allow_html=True,
    )
    
        # When the form is submitted, authenticate the user
    if submit_button:
        if selected in ["Signup", "Login"]:
            st.sidebar.empty()
        else:
            pass
        user = validate_user(username, password)
        if user:
                # Set session state for logged-in user
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.success("Login successful! Redirecting to the main page...")
            st.rerun()  # Optionally, you can redirect to another page here
        else:
            st.error("Invalid username or password.")
    


def signup_page():
    leo.bg_image('https://i.pinimg.com/originals/ff/04/31/ff0431d11ff6b73e937280252f58f371.gif')
    
    st.markdown("""<center><h1>Signup</h1></center>""",unsafe_allow_html=True)
    
    name = st.text_input("Name")
    username = st.text_input("Username")
    email = st.text_input("Email")

    password = st.text_input("Password", type="password",placeholder="enter you valid password")
    if st.button("Signup"):

        if len(password) < 8:
            st.error("Please enter a password with at least 8 characters.")
        else:
            if register_user(name, username, password, email):
                st.success("Signup successful! You can now log in.")
            else:
                st.error("Username already exists. Try another one.")


# Sidebar for navigation using a dropdown
with st.sidebar:
    leo.sidebar_bg_image('https://t3.ftcdn.net/jpg/02/32/99/54/360_F_232995426_xAopAAEterBrZhcC1CXLVtCF6RhYF5Z3.jpg')
    st.markdown("""
    <h1 style='font-size: 30px; font-family: "Arial", sans-serif;'>Login or Signup</h1>
""", unsafe_allow_html=True)
    
    if st.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["page"] = "login"
        st.rerun()
    




# Display the page based on the user's state
if st.session_state["logged_in"]:
    fac.main()
else:
    if st.session_state["page"] == "login":
        login_page()
    elif st.session_state["page"] == "signup":
        signup_page()
