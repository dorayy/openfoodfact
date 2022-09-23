from re import S
import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import plotly.express as px


st.title('Allergies page')
# Requete pour recuperer les données du produit par id
def get_allergies():
    url = 'https://world.openfoodfacts.org/allergens.json?limit=11'
    res = requests.get(url)
    return res.json()


allergies = get_allergies()
name = [i['name'] for i in allergies['tags']]
countProduct = [i['products'] for i in allergies['tags']]
listAllergies = pd.DataFrame({'name': name, 'countProduct': countProduct})

bouffeAutre = listAllergies.iloc[5:].countProduct.sum(axis=0)
newList = listAllergies.iloc[:5]
autre = newList.loc[5] = ['Autre', bouffeAutre]
newList.append(autre, ignore_index=True)

fig1, ax1 = plt.subplots()
ax1.pie(newList['countProduct'], labels=newList['name'], autopct='%1.1f%%', startangle=90)
ax1.axis('equal')

st.pyplot(fig1)