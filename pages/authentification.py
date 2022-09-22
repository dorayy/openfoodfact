 # streamlit_app.py
from operator import iconcat
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

def check_password(rows, name, pwd):
    for row in rows:
        if(row[0] == name and row[1] == pwd):
            st.write("Welcome " + name + "!")
            st.success('Vous allez être redirigé vers la page product sinon cliquez sur le lien à votre gauche !')
            st.balloons()
            return
    st.warning("Incorrect username/password")

st.title('Authentification')
name = st.text_input("Name")
pwd = st.text_input("Password", type="password")
rows = run_query("SELECT name, pwd from user where name='" + name + "';")
st.button("Connection", on_click=check_password, args=(rows, name, pwd))
