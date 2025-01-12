import streamlit as st
import sqlite3
import main1 as fac
import bg_image as bg
import naanthan_da_leo as leo 
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
        c.execute('INSERT INTO users (name, username, password, email) VALUES (?, ?, ?, ?)',
                  (name, username, password, email))
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
def main_page():
    
    fac.main()
    if st.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["page"] = "login"
        st.rerun()


# Login and signup pages
def login_page():
    st.markdown("""
    <style>
    .stMain {
        background-image: url('https://w0.peakpx.com/wallpaper/314/578/HD-wallpaper-dark-bg-bg-wp-abstract-dark.jpg'); /* Local background image */
        background-size: cover;
    }
    .stMainBlockContainer {
        background-image: url('https://static.vecteezy.com/system/resources/previews/007/115/713/original/the-old-vintage-black-brick-wall-background-with-lighting-decoration-and-dark-tone-style-for-background-design-concept-free-photo.jpg'); /* Local login image */
        background-size: cover;
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
    st.markdown('''<center><h2 id="login" style="color: blue;">STAFF LOGIN</h2></center>''', unsafe_allow_html=True)
    
    username = st.text_input("username",placeholder="Username")
    password = st.text_input("Password", type="password",placeholder="password")
    if st.button("Login"):
        user = validate_user(username, password)
        if user:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.success("Login successful! Redirecting to the main page...")
            st.rerun()
        else:
            st.error("Invalid username or password.")


def signup_page():
    #bg.local_bg_image()
    leo.bg_image('https://w0.peakpx.com/wallpaper/314/578/HD-wallpaper-dark-bg-bg-wp-abstract-dark.jpg')
    st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] > .main {
        background: url('leo.jpg'); /* Local background image */
        background-size: cover;
    }
    </style>
    """,unsafe_allow_html=True)

    st.header("Signup")
    name = st.text_input("Name")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Signup"):
        if register_user(name, username, password, email):
            st.success("Signup successful! You can now login.")
        else:
            st.error("Username already exists. Try another one.")


# Sidebar for navigation using a dropdown
with st.sidebar:
    option = ["login", "signup"]
    select = st.selectbox("Login or Signup", option)

    if select == "login":
        st.session_state["page"] = "login"
    else:
        st.session_state["page"] = "signup"

# Display the page based on the user's state
if st.session_state["logged_in"]:
    main_page()
else:
    if st.session_state["page"] == "login":
        login_page()
    elif st.session_state["page"] == "signup":
        signup_page()
