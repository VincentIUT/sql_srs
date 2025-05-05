import streamlit as st
import pandas as pd
import duckdb as db


st.write('Hello world !')
data = {"a": [1, 2, 3], "b": [4, 5, 6]}
df = pd.DataFrame(data)

tab1, tab2 = st.tabs(["opening", "Dog"])

with tab1:
    sql_query = st.text_area(label="entrez votre texte")
    req = db.query(sql_query).df()
    st.write(f"Vous avez entré la query suivante : {sql_query}")
    st.dataframe(req)

with tab2:
    st.header("A dog")
    st.image("https://cdn.futura-sciences.com/cdn-cgi/image/width=1920,quality=50,format=auto/sources/images/actu/esperance-vie-chiens-chiot-golden-retriever.jpg", width=200)

