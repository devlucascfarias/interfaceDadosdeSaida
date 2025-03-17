import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.ndimage import gaussian_filter

data_file = st.sidebar.file_uploader("Faça upload do arquivo CSV", type=["csv"])
if data_file is not None:
    df = pd.read_csv(data_file)
    df = df.rename(columns={"Points:1": "y", "U:1": "U_measured"})

st.sidebar.title("Parâmetros do Jato")
const_u = st.sidebar.number_input("Velocidade máxima inicial (const_u)", min_value=0.1, max_value=10.0, value=1.5, step=0.1)
const_y = st.sidebar.number_input("Taxa de crescimento da largura do jato (const_y)", min_value=0.01, max_value=1.0, value=0.11, step=0.01)
x_0 = st.sidebar.number_input("Origem virtual do jato (x_0)", min_value=-10.0, max_value=10.0, value=0.0, step=0.1)

y_min = st.sidebar.number_input("Valor mínimo de y", min_value=0.1, max_value=10.0, value=1.0, step=0.1)
y_max = st.sidebar.number_input("Valor máximo de y", min_value=10.0, max_value=100.0, value=15.0, step=1.0)
n_points = st.sidebar.number_input("Número de pontos", min_value=10, max_value=500, value=100, step=10)

st.sidebar.title("Opções de Visualização")
show_measured = st.sidebar.checkbox("Exibir Dados Medidos", value=True)
show_smoothed = st.sidebar.checkbox("Exibir Dados Suavizados", value=True)

smooth_factor = st.sidebar.slider("Fator de Suavização", min_value=0.1, max_value=5.0, value=1.0, step=0.1)

def u_max(y):
    return const_u / (y - x_0)

def y_half(y):
    return const_y * (y - x_0)

y_values = np.linspace(y_min, y_max, n_points)
u_values = u_max(y_values)
y_half_values = y_half(y_values)

fig, axs = plt.subplots(1, 2, figsize=(10, 5))

axs[0].plot(y_values, u_values, label="Teórico", color='b')

if data_file is not None:
    if show_measured:
        axs[0].scatter(df["y"], df["U_measured"], color='gray', label="Medido")
    
    if show_smoothed:
        smoothed_U_measured = gaussian_filter(df["U_measured"], sigma=smooth_factor)
        axs[0].plot(df["y"], smoothed_U_measured, color='r', label="Medido Suavizado")

axs[0].set_xlabel("y (altura)")
axs[0].set_ylabel("Velocidade máxima")
axs[0].set_title("Decaimento da Velocidade na Linha Central")
axs[0].legend()
axs[0].grid()

axs[1].plot(y_values, y_half_values, label=r'$y_{0.5}(y)$', color='r')
axs[1].set_xlabel("y (altura)")
axs[1].set_ylabel("Largura de meia-velocidade")
axs[1].set_title("Crescimento da Largura do Jato")
axs[1].legend()
axs[1].grid()

st.pyplot(fig)
