from itertools import product
from os import stat
from pprint import pprint
import matplotlib.pyplot as plt
from xml.dom.minidom import TypeInfo
import streamlit as st
import pandas as pd
import requests

st.markdown("<h1 style='text-align: center; color: black;  margin-bottom:100px'>Quelques stats avec openfoodfact</h1>", unsafe_allow_html=True)


# récup les données
def get_product():
    url = 'https://world.openfoodfacts.org/products.json?page_size=100'
    res = requests.get(url)
    return res.json()

stat_product = get_product()

stats = [i['manufacturing_places_tags'] for i in stat_product['products']]
nom_stats = [y['product_name'] for y in stat_product['products']]
# footprint = [k['carbon_footprint_percent_of_known_ingredients'] for k in stat_product['products']]
# nutrition_grade = [n['nutrition_grades'] for n in stat_product['products']]
# st.write(stat_product['products']['nutriscore_grade'])
# lstat = st.table({'nom du produit': nom_stats,'stats': stats})

# Init dataframe
df = pd.DataFrame(stat_product['products'])
df = df[['carbon_footprint_percent_of_known_ingredients', 'nutriscore_grade']]
df = df.dropna(subset=["carbon_footprint_percent_of_known_ingredients","nutriscore_grade"])
empreinte  =  df.set_index("carbon_footprint_percent_of_known_ingredients")
st.markdown("<h1 style='text-align: center; color: black;  margin-bottom:25px'>L'empreinte carbone</h1>", unsafe_allow_html=True)
st.bar_chart(empreinte)

stat_location = pd.DataFrame({'nom_stats':nom_stats,'stats': stats})


nb_stat_location = stat_location['stats'].value_counts()
st.markdown("<h1 style='text-align: center; color: black; margin-bottom:25px'>Provenance des produits</h1>", unsafe_allow_html=True)
st.bar_chart(nb_stat_location)

# st.line_chart(footprint)

