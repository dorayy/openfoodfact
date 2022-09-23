 # streamlit_app.py
from operator import truediv
import streamlit as st
import mysql.connector

# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    return mysql.connector.connect(**st.secrets["mysql"])

conn = init_connection()

# Perform query.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

@st.experimental_memo(ttl=600)
def run_query_insert(query):
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        return True
    except:
        return False
    

def check_password(rows, name, pwd):
    for row in rows:
        if(row[0] == name and row[1] == pwd):
            st.write("Welcome " + name + "!")
            st.success('Vous allez être redirigé vers la page product sinon cliquez sur le lien à votre gauche !')
            st.balloons()
            return
    st.warning("Incorrect username/password")

def verify_user(name, mail):
    query = "SELECT * FROM user WHERE name = '" + name + "' OR mail = '" + mail + "'"
    rows = run_query(query)
    if(len(rows) != 0):
        st.warning("This username or mail already exist")
        return False
    else:
        return True

def insert_user(name, mail, pwd):
    if(verify_user(name, mail)):
        query = "INSERT INTO user (name, mail, pwd) VALUES ('" + name + "', '" + mail + "', '" + pwd + "')"
        succes = run_query_insert(query)
        if(succes):
            st.success("User created successfully")
        else:
            st.warning("User creation failed")

st.title('Authentification')
st.text('Veuillez vous authentifier pour accéder à la page product')
name = st.text_input("Name")
pwd = st.text_input("Password", type="password")
rows = run_query("SELECT name, pwd from user where name='" + name + "';")
st.button("Connection", on_click=check_password, args=(rows, name, pwd))

st.text('Si vous n\'avez pas de compte, veuillez vous inscrire')
st.text('Veuillez renseigner les champs suivants')
new_name = st.text_input("Name inscription")
new_mail = st.text_input("Mail inscription")
new_pwd = st.text_input("Password inscription", type="password")
new_pwd2 = st.text_input("Repeat Password", type="password")

if(new_pwd == new_pwd2 and new_pwd != "" and new_pwd2 != ""):
    st.button("Inscription", on_click=insert_user, args=(new_name, new_mail, new_pwd))
else:
    st.warning("Les mots de passe ne correspondent pas")