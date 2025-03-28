import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.ndimage import gaussian_filter

data_file = st.sidebar.file_uploader("Faça upload do arquivo CSV", type=["csv"])
df = None  

if data_file is not None:
    df = pd.read_csv(data_file)
    df = df.rename(columns={"Points:1": "x", "U:0": "U_x", "U:1": "U_y", "U:2": "U_z"})
    df["x"] = 15 - df["x"] 
    df["U_magnitude"] = np.sqrt(df["U_x"]**2 + df["U_y"]**2 + df["U_z"]**2)

st.sidebar.title("Opções de Visualização")
show_measured = st.sidebar.checkbox("Exibir Dados Medidos", value=False)
show_smoothed = st.sidebar.checkbox("Exibir Dados Suavizados", value=True)

smooth_factor = st.sidebar.slider(
    "Fator de Suavização", 
    min_value=0.1, 
    max_value=5.0, 
    value=1.0, 
    step=0.1
)

fig, ax = plt.subplots(1, 1, figsize=(6, 5))

if df is not None:
    if show_measured:
        ax.scatter(df["x"], df["U_magnitude"], color='gray', label="Medido")
    
    if show_smoothed:
        smoothed_U_measured = gaussian_filter(df["U_magnitude"], sigma=smooth_factor)
        ax.plot(df["x"], smoothed_U_measured, color='r', label="Medido Suavizado")

ax.set_xlabel("Posição")
ax.set_ylabel("Velocidade máxima (Magnitude)")
ax.set_title("Decaimento da Velocidade na Linha Central")
ax.legend()
ax.grid()
st.pyplot(fig)

if df is not None:
    st.subheader("Visualização do DataFrame")
    st.write(df)

if df is not None:
    x_min_select, x_max_select = st.sidebar.slider(
        "Selecione faixa de x",
        float(df["x"].min()), 
        float(df["x"].max()), 
        (float(df["x"].min()), float(df["x"].max()))
    )
    df_faixa = df[(df["x"] >= x_min_select) & (df["x"] <= x_max_select)]

    fig_faixa, ax_faixa = plt.subplots()
    ax_faixa.plot(df_faixa["x"], df_faixa["U_magnitude"], color='red')
    ax_faixa.set_title("Subconjunto de x")
    ax_faixa.set_xlabel("Posição")
    ax_faixa.set_ylabel("Velocidade máxima (Magnitude)")
    ax_faixa.legend()  
    ax_faixa.grid()
    st.pyplot(fig_faixa)

