import streamlit as st
import pandas as pd
import requests

def get_products(nbr_products, page):
    url = 'https://world.openfoodfacts.org/products.json&page_size='+str(nbr_products)+'&page='+str(page)+''
    response = requests.get(url)
    return response.json().get('products')

def get_number_products(number):
    url = 'https://world.openfoodfacts.org/products.json'
    response = requests.get(url)
    return response.json().get('count') / number

def dataframe_products(products):
    df = pd.DataFrame(columns= ['id', 'name', 'brands', 'allergens', 'categories', 'ecoscore_grade','ecoscore_score', 'expiration_date', 'image_url', 'nutriscore_grade', 'nutriscore_score','product_quantity', 'scans_n', 'stores'])

    for i in products:
        if i.get('id'):
            if (i.get('product_quantity')):
                product_quantity = int(i.get('product_quantity'))
            else:
                product_quantity = i.get('product_quantity')

            if (i.get('ecoscore_score')):
                ecoscore_score = int(i.get('ecoscore_score'))
            else:
                ecoscore_score = i.get('ecoscore_score')

            if (i.get('nutriscore_score')):
                nutriscore_score = int(i.get('nutriscore_score'))
            else:
                nutriscore_score = i.get('nutriscore_score')

            if (i.get('scans_n')):
                scans_n = int(i.get('scans_n'))
            else:
                scans_n = i.get('scans_n')

            df = df.append({'id' : i.get('id'),
                'name' : i.get('product_name'),
                'brands' : i.get('brands'), 
                'allergens' : i.get('allergens'), 
                'categories' : i.get('categories'), 
                'ecoscore_grade' : i.get('ecoscore_grade'), 
                'ecoscore_score' : ecoscore_score, 
                'expiration_date' : i.get('expiration_date'), 
                'image_url' : i.get('image_url'), 
                'nutriscore_grade' : i.get('nutriscore_grade'), 
                'nutriscore_score' : nutriscore_score, 
                'product_quantity' : product_quantity, 
                'scans_n' : scans_n, 
                'stores' : i.get('stores')                  
                },ignore_index = True)

    df.dropna()
    return df

def sort_products(df, name):
    if (name == False):
        return df
    else :
        df = df.sort_values(by=[name], ascending=True)
        return df

def displayProducts(nbr_of_products_per_page, columnFilter):
    st.session_state.page_number = 1
    last_page = get_number_products(nbr_of_products_per_page) 

    if 'count' not in st.session_state:
        st.session_state.count = 1

    prev, _ ,next = st.columns([1, 10, 1])

    def decrement_counter(decrement_value=0):
        if (st.session_state.count > 1):
            st.session_state.count -= decrement_value

    def increment_counter(increment_value=0):
        if (st.session_state.count < last_page):
            st.session_state.count += increment_value
    
    prev.button('Previous', on_click=decrement_counter, kwargs=dict(decrement_value=1))
    next.button('Next', on_click=increment_counter, kwargs=dict(increment_value=1))

    products = get_products(nbr_of_products_per_page, st.session_state.count)
    dfAll = dataframe_products(products)
    dfAll = sort_products(dfAll, columnFilter)
    st.write(dfAll) 
    st.write("Page : "+ str(st.session_state.count) +" sur "+ str(int(last_page)))

st.title('Projet Open Food Facts')
st.write('Products') 

df = pd.DataFrame(columns= ['id', 'name', 'brands', 'allergens', 'categories', 'ecoscore_grade','ecoscore_score', 'expiration_date', 'image_url', 'nutriscore_grade', 'nutriscore_score','product_quantity', 'scans_n', 'stores'])
st.session_state.filter = st.selectbox('Filter', df.columns)

reset, _ ,confirm = st.columns([1, 10, 1])

def selectFilter():
    st.session_state.filter = ""

def filterProducts():
    displayProducts(20, st.session_state.filter)

reset.button('Reset', on_click=selectFilter)
confirm.button('Confirm', on_click=filterProducts)

displayProducts(20, False)