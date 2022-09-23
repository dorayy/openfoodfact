import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

st.title('Product détail page')



# Requete pour recuperer les données du produit par id
def get_product(barcode):
    url = 'https://world.openfoodfacts.org/api/v0/product/' + barcode + '.json'
    res = requests.get(url)
    return res.json()

def show_page():
    # Affichage produit
    
    st.write("Code barre : ", product['code'])
    st.write("Nom : ", product['product']['product_name'])
    st.write("Marque : ", product['product']['brands'])
    st.write("Quantité : ", product['product']['quantity'])
    st.write("Nutriscore : ", product['product']['nutriscore_grade'])
    st.write("Catégorie : ", product['product']['categories'])
    st.write("Pays de fabrication : ", product['product']['countries'])
    st.image(product['product']['image_front_url'], width=200)

# Requete de recherche de substitut
def get_substitut(barcode):
    product = get_product(barcode)
    #nutriscore = product['product']['nutriscore_grade']
    category = product['product']['categories']
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
    show_page()

    if st.checkbox('Recherche des subsituts'):
        subsitutData = get_substitut(ean)

        # Init dataframe
        df = pd.DataFrame(subsitutData['products'])
        df = df[['id', 'product_name', 'nutriscore_grade']]

        ## Partie nettoyage

        # Filtre proposant les nutriscore supérieur à celui existant
        df = df[df['nutriscore_grade'] < product['product']['nutriscore_grade']]
        df = df.sort_values(by=['nutriscore_grade'])

        # Suppression des données incorrectes
        df = df.dropna(subset=['id', 'product_name', 'nutriscore_grade'])
        
        # String upper
        df['product_name'] = df['product_name'].str.upper()
        df['nutriscore_grade'] = df['nutriscore_grade'].str.upper()

        # Suppression des doublons
        df['product_name'] = df['product_name'].str.replace('-', ' ')
        df = df.drop_duplicates(subset=["product_name"], keep=False)

        # On affiche
        st.write("Les substituts trouvés  : ")
        st.write(df)

        # Le score
        st.write("Le graphique sur les différents classement nutriscore  : ")
        st.bar_chart(df , y="product_name", x="nutriscore_grade")
       
   
    if st.checkbox('Sauvegarder le résultat dans la base de données'):
        # Préparation des données
        df['id_research'] = product['code']
        dfResult = df[['id_research','id', 'product_name', 'nutriscore_grade']]
        dfResult.rename(columns={"id": "id_substitut"}, inplace=True)
        
        # Connexion à la base de données
        my_conn = create_engine("mysql+mysqldb://root:@localhost/openfoodsdata")

        sql = "SELECT * FROM results WHERE id_research = " + product['code']
        res = pd.read_sql(sql, my_conn)

        if not res.empty:
            st.write(res.to_html(), unsafe_allow_html=True)
        else:
            # Sauvegarde des données
            st.write("Ajouter le résultat dans la base de données")
            if st.button('Save'):
                dfResult.to_sql('results', my_conn, if_exists='append', index=False)
                st.success("Le résultat a été sauvegardé")


    