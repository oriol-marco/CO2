
# Proyecto de análisis de emisiones de CO2 con Streamlit

import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

# ----------------------------------------------------------------
# Get and load data
# ----------------------------------------------------------------

@st.cache()
def get_co2_data():
    url = 'https://github.com/owid/co2-data/raw/master/owid-co2-data.csv'
    return pd.read_csv(url)

st.set_page_config(layout='wide')

co2_df = get_co2_data()

# ----------------------------------------------------------------

st.title("World CO2 Emissions")
st.markdown("Los gráficos que se muestran a continuación hacen referencia a las emisiones de co2 a nivel global y por paises. También se pueden observar las emisiones generadas por diferentes industrias y comercio.")

st.markdown("A lo largo de la página se pueden observar diferentes gráficos y así, poder analizar las diferentes emisiones y su distribución geográfica por paises.")

# ----------------------------------------------------------------

st.header('Co2 emissions Dataframe')
st.markdown('En la siguiente entrada podemos observar la cabecera del dataframe que se ha utilizado para efectuar los siguientes análisis:')

st.dataframe(co2_df.head())

# ----------------------------------------------------------------

st.header('Global Co2 emissions and Co2 emissions per Capita')
st.markdown("En el gráfico de la izquierda, podemos observar la evolución de las emisiones totales de CO2 globales y las mismas clasificadas por paises. En el gráfico de la derecha podemos observar la misma visualización, esta vez con los datos de emisión de Co2 per capita")

# ----------------------------------------------------------------

default_countries = ['World', 'United States', 'China', 'United Kingdom', 'Canada']
countries = co2_df['country'].unique()

selected_countries = st.multiselect('Selecciona un país o grupo de paises', countries, default_countries)

col2, space1, col3 = st.columns((10,1,10))

with col2:
    
    df3 = co2_df.query('country in @selected_countries')
    fig = px.line(df3,"year","co2_per_capita",color="country")

    st.plotly_chart(fig, use_container_width=True)
    

with col3:
    
    df4 = co2_df.query('country in @selected_countries')
    fig = px.line(df3,"year","co2",color="country")

    st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------------------

st.header('Distribution and evolution of Co2 emissions')

st.markdown('Con el deslizador, selecciona el año y visualiza la evolución de las emisiones globales de Co2 y las emisiones de Co2 per capita')
      
year = st.slider('Selecciona el rango de años', 1750, 2020)

col4, space2, col5 = st.columns((10,1,10))

with col4:

    fig2 = px.choropleth(co2_df[co2_df['year']==year], locations='iso_code',
                    color="co2",
                    hover_name="country",
                    range_color=(0,300),
                    color_continuous_scale='viridis')
    st.plotly_chart(fig2, use_container_width=True)

with col5:

    fig3 = px.choropleth(co2_df[co2_df['year']==year], locations='iso_code',
                    color="co2_per_capita",
                    hover_name="country",
                    range_color=(0,10),
                    color_continuous_scale='viridis')
    st.plotly_chart(fig3, use_container_width=True)

# ----------------------------------------------------------------

col6, space3, col7 = st.columns((8,1,12))

with col6:
    st.header('Evolution of C02 emissions vs. population')
    st.markdown('Habitualmente se obtienen visualizaciones de las emisiones totales de Co2 per capita. En esta ocasión, realizamos un análisis de la relación de las emisiones de Co2 per capita contra el crecimiento de la población de un país. De esta forma, podemos determinar la relación del aumento de la población con el aumento de las emisiones, y ver si estas tienen una correlación lineal.')

with col7:
    countries = co2_df['country'].unique()

    selected_country = st.selectbox('Selecciona un país', countries)       

    df5 = co2_df.query('country in @selected_country')
    fig4 = px.bar(df5, x='year', y='population', 
                  hover_data=['co2_per_capita'],
                  color='co2_per_capita',
                  labels={'population':'Country Population'},
                )
    
    st.plotly_chart(fig4, use_container_width=True)