import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime as dt
from datetime import datetime


base="light"
backgroundColor="#e0d8d8"
secondaryBackgroundColor="#b5a1a1"


st.set_page_config(layout="wide", page_title="Restaurante Dona Nize", initial_sidebar_state="expanded", page_icon="🧊")

st.sidebar.header("Restaurante Dona Nize | Elisa Agro")

df = pd.read_csv("databaseElisa.csv", sep=";", decimal=",", thousands=".",
                 usecols=['data','fazenda', 'almoco', 'janta', 'cafe','lanche', 'total'],
                 index_col=None
                 ) 

st.markdown("""
        <style>
               .block-container {
                    padding-top: 0px;
                }
        </style>
            
            
        """, unsafe_allow_html=True)

df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y', errors='coerce')
df['data'] = df['data'].dt.date

mes_atual = dt.datetime.today().month
ano_atual = dt.datetime.today().year

default_start_date = dt.date(ano_atual, mes_atual, 1)

start_date = st.sidebar.date_input('DATA INÍCIO:', default_start_date, None, format="DD/MM/YYYY")
end_date = st.sidebar.date_input('DATA FIM:', None, format="DD/MM/YYYY")


st.sidebar.write("____")

if start_date:
    start_date = pd.Timestamp(start_date)
if end_date:
    end_date = pd.Timestamp(end_date)

col1, col2 = st.columns([2,1])
c = st.container()

if start_date or end_date:

    if 'data' in df.columns:
        
        if start_date is not None:
            dia_start = str(start_date.day)
            mes_start = str(start_date.month)
            ano_start = str(start_date.year)

        if end_date is not None:
            
            dia_end = str(end_date.day)
            mes_end = str(end_date.month)
            ano_end = str(end_date.year)
        
        if start_date and end_date:

            if start_date > end_date:
                st.warning('Data de início é maior que data de término!')
            else:
                periodo = dia_start + "/" + mes_start + "/" + ano_start + " - " + dia_end + "/" + mes_end + "/" + ano_end
                filtered_df = df[(df['data'] >= start_date) & (df['data'] <= end_date)]
        elif start_date:
            periodo = dia_start + "/" + mes_start + "/" + ano_start
            filtered_df = df[(df['data'] == start_date)]
        elif end_date:
            periodo = dia_end + "/" + mes_end + "/" + ano_end
            filtered_df = df[(df['data'] == end_date)]

        #################### Tabela Demostrativo Período ########################
        lista_fazenda = df['fazenda'].unique().tolist()
                
        qtd_almoco = filtered_df.groupby("fazenda")[["almoco"]].sum()

        qtd_janta = filtered_df.groupby("fazenda")[["janta"]].sum()

        qtd_cafe = filtered_df.groupby("fazenda")[["cafe"]].sum()

        qtd_lanche = filtered_df.groupby("fazenda")[["lanche"]].sum()

        qtd_almoco = qtd_almoco.reindex(lista_fazenda)
        qtd_janta = qtd_janta.reindex(lista_fazenda)
        qtd_cafe = qtd_cafe.reindex(lista_fazenda)
        qtd_lanche = qtd_lanche.reindex(lista_fazenda)

        lista_almoco = qtd_almoco["almoco"].tolist()
        lista_janta = qtd_janta["janta"].tolist()
        lista_cafe = qtd_cafe["cafe"].tolist()
        lista_lanche = qtd_lanche["lanche"].tolist()
                    
        #del(lista_fazenda[7])
        #del(lista_almoco[7])
        #del(lista_janta[7])
        #del(lista_cafe[7])
        #del(lista_lanche[7])  

        data = {
            "Fazenda": lista_fazenda,
            "Café": lista_cafe,
            "Almoço": lista_almoco,
            "Lanche": lista_lanche,
            "Janta": lista_janta
        }

        data_frame = pd.DataFrame(data)

        sums = {
            "Fazenda": "<b>TOTAL</b>",
            "Café": "<b>" + str('{0:,}'.format(int(data_frame["Café"].sum())).replace(',','.')) + "</b>",
            "Almoço": "<b>" + str('{0:,}'.format(int(data_frame["Almoço"].sum())).replace(',','.')) + "</b>",
            "Lanche": "<b>" + str('{0:,}'.format(int(data_frame["Lanche"].sum())).replace(',','.')) + "</b>",
            "Janta": "<b>" + str('{0:,}'.format(int(data_frame["Janta"].sum())).replace(',','.')) + "</b>"
                }

        data_frame = data_frame.append(sums, ignore_index=True)

        fig = go.Figure(data=[go.Table(
            header=dict(values=list(data_frame.columns),
                fill_color='firebrick',
                line_color="lightgrey",
                font_color="white",
                align='center'),
            cells=dict(values=[data_frame.Fazenda, data_frame.Café, data_frame.Almoço, data_frame.Lanche, data_frame.Janta],
                fill=dict(color=['linen', 'white','whitesmoke','white','whitesmoke']),                                
                line_color="lightgrey",
                font_color="black",
                align='center'))
            ])

        fig.update_layout(title={ 'text': "Demostrativo: " + periodo, 'y':0.76, 'x':0.0, 'xanchor': 'left', 'yanchor': 'top'})
        fig.update_layout(height = 420, margin=dict(r=10,t=140))
        col1.plotly_chart(fig, use_container_width=True, automargin=True)

        

        #################### Gráfico Fazenda Período ########################
        fazenda_total = filtered_df.groupby("fazenda")[["total"]].sum().reset_index()
        fig_venda_fazenda = px.pie(fazenda_total, names="fazenda", values="total",color_discrete_sequence=px.colors.sequential.RdBu)
        fig_venda_fazenda.update_layout(width=600, height=400)
        fig_venda_fazenda.update_traces(textposition='inside', textinfo='percent+label')
        fig_venda_fazenda.update_layout(margin=dict(l=10, b=50,t=140))
        col2.plotly_chart(fig_venda_fazenda, use_container_width=True)

        #################### Gráfico Venda Mês Atual ########################
        if df['data'].dtype != 'datetime64[ns]':
            df['data'] = pd.to_datetime(df['data'], errors='coerce')

            ano_atual = dt.datetime.now().year
            mes_atual = dt.datetime.now().month

            def switch(mes_atual):
                if mes_atual == 1:
                    return "janeiro"
                elif mes_atual == 2:
                    return "Fevereiro"
                elif mes_atual == 3:
                    return "Março"
                elif mes_atual == 4:
                    return "Abril"
                elif mes_atual == 5:
                    return "Maio"
                elif mes_atual == 6:
                    return "Junho"                    
                elif mes_atual == 7:
                    return "Julho"
                elif mes_atual == 8:
                    return "Agosto"
                elif mes_atual == 9:
                    return "Setembro"
                elif mes_atual == 10:
                    return "Outubro"
                elif mes_atual == 11:
                    return "Novembro"
                elif mes_atual == 12:
                    return "Dezembro"                                                                

            df_mes = df[(df['data'].dt.month == mes_atual) & (df['data'].dt.year == ano_atual)]

            venda_total = df_mes.groupby("data")[["total"]].sum().reset_index()
            fig_venda_mes = px.bar(venda_total, x="data", y="total", color_discrete_sequence=px.colors.sequential.RdBu, title="Visão Geral: " + switch(mes_atual) + "/" + str(ano_atual),
                                    text_auto='.2f',
                                    )
                
            fig_venda_mes.update_traces(textangle=0, textposition="outside", cliponaxis=False)
            fig_venda_mes.update_layout(margin=dict(t=50))

            c.plotly_chart(fig_venda_mes, use_container_width=True)

            
    else:

        st.warning('A coluna "data" não foi encontrada na base fornecida.')
