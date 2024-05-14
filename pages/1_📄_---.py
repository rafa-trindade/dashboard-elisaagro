import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(
    layout="wide",
    page_title="Gestão e Análise | Rafael Trindade", 
    initial_sidebar_state="expanded", 
    page_icon="📊")

hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}    
                footer {visibility: hidden;}
                header {visibility: hidden;} 
                </style>
                """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.markdown(
    """
    <style>
        [data-testid="stSidebarNav"] {
            background-image: url(https://i.postimg.cc/52vw7RW6/streamlit-Logo2.png);
            background-repeat: no-repeat;
            padding-top: 37px;
            background-position: 18px 55px;
            position: relative;
        }
    </style>
    """,
    unsafe_allow_html=True,
)
 
