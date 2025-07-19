
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Balance de Masa del Hidrocarburo Derramado", layout="centered")

st.title("Balance de Masa del Hidrocarburo Derramado")

# 1. Ingreso de datos del derrame
st.markdown("### 1. Datos del derrame")

Q = st.number_input("Caudal de descarga (L/min)", min_value=0.0, value=100.0)
t = st.number_input("Duración del derrame (min)", min_value=0.0, value=60.0)
V_d = Q * t

st.success(f"Volumen total derramado: {V_d:.1f} L")

# 2. Métodos utilizados
st.markdown("### 2. Métodos utilizados")
metodos = st.multiselect(
    "Seleccione los métodos aplicados:",
    ["Barreras de contención", "Skimmers", "Absorbentes", "Dispersantes"]
)

v_skimmer = 0
v_rec = 0
factor_dispersante = 1.0

if "Skimmers" in metodos:
    v_skimmer = st.number_input("Volumen recuperado por skimmers (L)", min_value=0.0, value=0.0)

if "Absorbentes" in metodos:
    m_rec = st.number_input("Masa total del absorbente recuperado (kg)", min_value=0.0, value=0.0)
    m_abs = st.number_input("Masa seca del absorbente (kg)", min_value=0.0, value=0.0)
    C_abs = st.number_input("Capacidad máxima de absorción (L/kg)", value=4.0)
    eta = st.slider("Porcentaje de saturación efectiva (%)", 0, 100, 85) / 100
    V_rec = m_abs * C_abs * eta

if "Dispersantes" in metodos:
    aumento_disc = st.slider("Aumento estimado de disolución por dispersante (%)", 0.0, 1.0, 0.1)
    factor_dispersante = 1 + aumento_disc

# 3. Condiciones ambientales
v_viento = st.slider("Velocidad del viento (m/s)", 0.0, 10.0, 3.0)
altura_ola = st.slider("Altura significativa de ola (m)", 0.0, 5.0, 1.5)
T_agua = st.slider("Temperatura del agua (°C)", 0, 30, 14)

# 4. Estimación de pérdidas físicas
t_horas = t / 60
f_evap = 0.0001 * (v_viento ** 0.78) * (t_horas ** 0.5)
f_evap = min(f_evap, 0.9)
V_evap = V_d * f_evap

V_disperso = 0.012 * V_d * factor_dispersante
V_disu = 0.005 * V_d * factor_dispersante
V_bio = 0.02 * V_d * factor_dispersante

V_rem = V_d - (v_skimmer + V_rec + V_evap + V_disperso + V_disu + V_bio)

# 5. Visualización
st.markdown("### 5. Visualización del Balance de Masa")

labels = ["Recuperado Skimmer", "Absorbentes", "Evaporado", "Dispersado", "Disuelto", "Biodegradado", "Remanente"]
values = [v_skimmer, V_rec, V_evap, V_disperso, V_disu, V_bio, V_rem]

chart_type = st.radio("Seleccione el tipo de gráfico:", ["Torta", "Barras", "Barras Apiladas"])

if chart_type == "Torta":
    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
    ax.axis("equal")
    st.pyplot(fig)

elif chart_type == "Barras":
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(labels, values)
    ax.set_ylabel("Volumen (L)")
    ax.set_xticklabels(labels, rotation=45, ha="right")
    st.pyplot(fig)

elif chart_type == "Barras Apiladas":
    fig, ax = plt.subplots(figsize=(10, 5))
    bar_bottoms = np.cumsum([0] + values[:-1])
    ax.bar(["Derrame"], values, bottom=bar_bottoms)
    for i, v in enumerate(values):
        ax.text(0, bar_bottoms[i] + v / 2, f"{labels[i]}\n{v:.1f} L", ha="center")
    ax.set_ylabel("Volumen (L)")
    st.pyplot(fig)








