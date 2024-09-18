import pandas as pd
import streamlit as st
import datetime as dt

@st.cache_data
def load_database():
    df = pd.read_excel('./data/f1.xlsx')
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['car_position'].astype(str)
    df['car_points'].astype(str)
    df['laps'].astype(str)
    df['Order Year'] = df['date'].dt.year
    df['Order Month'] = df['date'].dt.month
    #df['Dispatch Year'] = df['Dispatch Date'].dt.year
    #df['Dispatch Month'] = df['Dispatch Date'].dt.month
    # df = df.drop(columns=['Row ID', 'Order ID', 'Product Name', 'Product ID', 'Sigla', 'Country', 'Lat', 'Lng'])
    return df


st.set_page_config(page_title="Gestão do Conhecimento", layout="wide")
st.session_state['df'] = load_database()
st.session_state['dimensao'] = [
    'forename', 'surname', 'country', 'location', 'circuit_name', 'race_name'
]
#st.session_state['corridas'] = [
#    'raceId', 'round', 'name'
#]
#st.session_state['pilotos'] = [
#    'forename', 'nationality', 'dob'
#]
#st.session_state['equipe'] = [
#    'name', 'nationality', 'constructorId'
#]
#st.session_state['resultados'] = [
#    'position', 'points', 'laps','time'
#]
st.session_state['dimensao_tempo'] = ['time', 'year', 'date',]
st.session_state['medida'] = ['car_position', 'car_points', 'laps']
st.session_state['agregador'] = ['sum', 'mean', 'count', 'min', 'max']
st.title('Gestão do Conhecimento')

pg = st.navigation(
    {
        "Introdução": [
            st.Page(page='introducao/tabela.py', title='Tabela', icon=':material/house:'),
            st.Page(page='introducao/cubo.py', title='Cubo', icon=':material/help:'),
            st.Page(page='introducao/dashboard.py', title='Dashboard', icon=':material/help:'),
            st.Page(page='introducao/visualizacao.py', title='Visualização', icon=':material/help:'),
        ],
        "Visualização": [
            st.Page(page='visualizacao/descritiva.py', title='Análise Descritiva',
                    icon=':material/house:'),
            st.Page(page='visualizacao/diagnostica.py', title='Análise Diagnóstica',
                    icon=':material/house:'),
            st.Page(page='visualizacao/preditiva.py', title='Análise Preditiva',
                    icon=':material/house:'),
            st.Page(page='visualizacao/prescritiva.py', title='Análise Prescritiva',
                    icon=':material/house:'),
        ]
    }
)
pg.run()
