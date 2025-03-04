import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

#Leer datos
goleadores = pd.read_csv('C:/Users/admin/Desktop/Streamlit/goalscorers.csv')

# Asegurar que todos los valores en 'scorer' sean cadenas y manejar nulos
goleadores['scorer'] = goleadores['scorer'].fillna('Desconocido').astype(str)


with st.sidebar:
    local = st.multiselect('Equipo Local',sorted(goleadores['home_team'].unique()))
    visitante = st.multiselect('Equipo Visitante', sorted(goleadores['away_team'].unique()))
    ganador = st.multiselect('Equipo Ganador', sorted(goleadores['team'].unique()))
    goleador = st.multiselect('Goleador', sorted(goleadores['scorer'].unique()))
    
def filter_data(goleadores, local, visitante, ganador, goleador):
    df_copy = goleadores.copy()

    if len(local) > 0:
        df_copy = df_copy[df_copy['home_team'].isin(local)]
    if len(visitante) > 0:
        df_copy = df_copy[df_copy['away_team'].isin(visitante)]

    if len(ganador) > 0:
        df_copy = df_copy[df_copy['team'].isin(ganador)]
        
    if len(goleador) > 0:
        df_copy = df_copy[df_copy['scorer'].isin(goleador)]
    
    return df_copy

st.title("Goleadores")
st.subheader("Análisis de enfrentamientos y goleadores")

df_ = filter_data(goleadores, local, visitante, ganador, goleador)

total_goles = len(df_)

total_goleadores = df_['scorer'].nunique()

goals_90th_minute = len(df_[df_['minute'] == 90])

percentage_90th_minute = (goals_90th_minute / total_goles) * 100 if total_goles > 0 else 0

# Crear columnas
col1, col2, col3, col4 = st.columns(4)

# Usar las columnas para mostrar métricas
col1.metric("# Total Goles", f"{total_goles:,.0f}")
col2.metric("# Jugadores", f"{total_goleadores:,.0f}")
col3.metric("Goals scored in the 90th minute", f"{goals_90th_minute:,.0f}")
col4.metric("Percentage of goals in the 90th minute", f"{percentage_90th_minute:,.0f}")

##############################
    
df_['scorer'] = df_['scorer'].fillna('Unknown').astype(str)
    
#############################    
# Eliminar filas con goles en contra
goleadores_a_favor = df_[df_['own_goal'] == 0]

# Contar los goles por jugador
goles_por_jugador = goleadores_a_favor.groupby('scorer')['scorer'].count().sort_values(ascending=False)

st.subheader("Jugadores con más goles")
st.dataframe(goles_por_jugador.head(10))

###########################    
    
# Agrupar por jugador, partido y contar los goles en cada partido
goles_por_partido = goleadores_a_favor.groupby(['scorer', 'date'])['scorer'].count().reset_index(name='goles')

# Encontrar el máximo número de goles anotados en un solo partido por cada jugador
max_goles_partido = goles_por_partido.loc[goles_por_partido.groupby('scorer')['goles'].idxmax()]

# Ordenar por la cantidad de goles de mayor a menor
max_goles_partido = max_goles_partido.sort_values('goles', ascending=False)

# Mostrar los jugadores con la mayor cantidad de goles en un partido y en qué partido lo hicieron
st.subheader("Top 10 jugadores con más goles en un partido")
st.dataframe(max_goles_partido[['scorer', 'date', 'goles']].head(10))

################################ 
# Lista de países únicos en el dataset
paises_disponibles = df_['team'].unique()

# Selector de país
pais = st.selectbox("Seleccione un país:", options=paises_disponibles)

# Filtrar los datos según el país y calcular los goles por penal
ganados_por_penal = len(df_[(df_['team'] == pais) & (df_['penalty'] == True)])

# Mostrar el resultado
st.write(f"Número de goles por penal de {pais}: {ganados_por_penal}")