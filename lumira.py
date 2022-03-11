import streamlit as st
import pandas as pd
import altair as alt
from multipage import MultiPage
import Alumina_from_factories, Alumina_from_ports, Alumina # import your pages here

# Настройки среды
st.set_page_config(layout="wide")
    
# Create an instance of the app 
app = MultiPage()

# Title of the main page
#st.title("Data Storyteller Application")

# Add all your applications (pages) here
app.add_page("Отгрузка с заводов ГД", Alumina_from_factories.app)
app.add_page("Поступление и перевалка в портах", Alumina_from_ports.app)
app.add_page("Ост.на заводах и в пути", Alumina.app)

# The main app
app.run()
