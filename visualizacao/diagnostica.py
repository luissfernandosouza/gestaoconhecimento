diagnostico.py


import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from streamlit_extras.metric_cards import style_metric_cards
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from itertools import combinations

style_metric_cards(
border_left_color="#3D5077",
background_color="#F0F2F6",
border_size_px=3,
border_color = "#CECED0",
border_radius_px = 20,
box_shadow=True)

cols = st.columns(4)
coluna = cols[0].selectbox(
'Dimensões Coluna',
st.session_state['dimensao']
)
conteudo = cols[1].selectbox(
'Classe:',
st.session_state['df'][coluna].unique()
)
medida = cols[2].selectbox(
'Medida',
st.session_state['medida']
)
mes = cols[3].selectbox(
'Mês',
st.session_state['df'][['Order Month']].sort_values(by='Order Month').drop_duplicates()
)
mes_atual = st.session_state['df'][
(st.session_state['df']['Order Year'] == 2023) & (st.session_state['df']['Order Month'] == mes)
]
cols = st.columns([1,3])
cols[0].subheader(f'Métrica de {medida} no mês {mes}')
if mes == 1:
cols[0].metric(
label=f'{medida} em relação ao mês anterior',
value=round(mes_atual[medida].sum(), 2)
)
else:
mes_anterior = st.session_state['df'][
(st.session_state['df']['Order Year'] == 2023) & (st.session_state['df']['Order Month'] == mes - 1)
]
cols[0].metric(
label=f'{medida} em relação ao mês anterior',
value=round(mes_atual[medida].sum(), 2),
delta=str(round(mes_atual[medida].sum() - mes_anterior[medida].sum(), 2)),
)
mes_ano_anterior = st.session_state['df'][
(st.session_state['df']['Order Year'] == 2022) & (st.session_state['df']['Order Month'] == mes)
]
cols[0].metric(
label=f'{medida} em relação ao mês no ano anterior',
value=round(mes_atual[medida].sum(), 2),
delta=str(round(mes_atual[medida].sum() - mes_ano_anterior[medida].sum(), 2)),
)
cols[0].subheader(f'Comparativo em {coluna}')
cols[0].plotly_chart(
px.box(
mes_atual,
x=coluna,
y=medida
)
)

with cols[1]:
cols[1].subheader(f'Indicador de {medida} em {coluna}({conteudo}) no mês {mes}')
meses = st.session_state['df'][
st.session_state['df'][coluna] == conteudo
].groupby(['Order Year', 'Order Month'])[medida].sum().reset_index()
fig = go.Figure(
go.Indicator(
mode="number+gauge+delta",
gauge={
'shape': "bullet",
'axis': {
'visible': True,
'range': [
meses[medida].min(),
meses[medida].max()
]
},
'steps': [
{'range': [meses[medida].min(), meses[medida].quantile(0.25)], 'color': "salmon"},
{'range': [meses[medida].quantile(0.25), meses[medida].quantile(0.50)], 'color': "lightsalmon"},
{'range': [meses[medida].quantile(0.50), meses[medida].quantile(0.75)], 'color': "ivory"},
{'range': [meses[medida].quantile(0.75), meses[medida].max()], 'color': "linen"},
],
'threshold': {
'line': {'color': "red", 'width': 4},
'thickness': 0.75,
'value': meses[medida].mean()
},
'bar': {'color': "blue"}
},
delta={'reference': meses[medida].mean()},
value=mes_atual[mes_atual[coluna] == conteudo][medida].sum(),
domain={'x': [0.2, 1], 'y': [0, 1]},
title={'text': f'{conteudo}'},
)
)
fig.update_layout(height=250)
cols[1].plotly_chart(fig)