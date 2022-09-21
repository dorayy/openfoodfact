import streamlit as st
import pandas as pd
import requests
import openfoodfacts


st.title('Projet Open Food Facts')
st.write('Product détail page') 

# Requete pour recuperer les données du produit par id
def get_product(barcode):
    url = 'https://world.openfoodfacts.org/api/v0/product/' + barcode + '.json'
    response = requests.get(url)
    return response.json()

# Test avec l'id du nutella
product = get_product('3017620422003')