from pprint import pprint
from xml.dom.minidom import TypeInfo
import streamlit as st
import pandas as pd
import requests


st.title('Product détail page')

# Requete pour recuperer les données du produit par id
def get_product(barcode):
    url = 'https://world.openfoodfacts.org/api/v0/product/' + barcode + '.json'
    res = requests.get(url)
    return res.json()

# Requete de recherche de substitut
def get_substitut(barcode):
    product = get_product(barcode)
    #nutriscore = product['product']['nutriscore_grade']
    category = product['product']['categories']
    print(category)
    url = 'https://world.openfoodfacts.org/cgi/search.pl?search_terms=' + category + '&search_simple=1&action=process&json=1'
    res = requests.get(url)
    return res.json()


# Search bar avec bouton
search_bar = st.text_input('Rechercher un produit', '')
search_button = st.button('Rechercher')

if search_button:
    st.experimental_set_query_params(ean=search_bar)

if st.experimental_get_query_params():
    # Récupération des paramètres de l'onglet
    ean = st.experimental_get_query_params()
    ean = ean.get('ean')[0]
    product = get_product(ean)

    # Affichage produit
    st.write("Code barre : ", product['code'])
    st.write("Nom : ", product['product']['product_name'])
    st.write("Marque : ", product['product']['brands'])
    st.write("Quantité : ", product['product']['quantity'])
    st.write("Nutriscore : ", product['product']['nutriscore_grade'])
    st.write("Catégorie : ", product['product']['categories']) 

    if st.button('Recherche des subsituts'):
        subsitutData = get_substitut(ean)

        # Init dataframe
        df = pd.DataFrame(subsitutData['products'])
        df = df[['product_name', 'nutriscore_grade', 'id']]
        # Filtre proposant les nutriscore supérieur à celui existant
        df = df[df['nutriscore_grade'] < product['product']['nutriscore_grade']]
        df = df.sort_values(by=['nutriscore_grade'])
        st.write(df)