
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(layout="wide")
st.title("Balance de Masa del Hidrocarburo Derramado")

# 1. Datos del derrame
st.markdown("### 1. Datos del derrame")
Q = st.number_input("Caudal de derrame (L/min)", min_value=0.0, value=50.0)
t = st.number_input("Duración del derrame (min)", min_value=0.0, value=60.0)
V_d = Q * t
st.success(f"**Volumen total derramado: {V_d:.1f} L**")

# 2. Métodos utilizados
st.markdown("### 2. Métodos utilizados")
metodos = st.multiselect(
    "Seleccione los métodos aplicados:",
    ["Barreras de contención", "Skimmers", "Absorbentes", "Dispersantes"]
)

V_skimmer = 0
V_rec = 0
factor_dispersante = 1.0

if "Skimmers" in metodos:
    V_skimmer = st.number_input("Volumen recuperado por skimmers (L)", min_value=0.0, value=500.0)

if "Absorbentes" in metodos:
    m_rec = st.number_input("Masa total del absorbente recuperado (kg)", min_value=0.0, value=100.0)
    m_abs = st.number_input("Masa seca del absorbente (kg)", min_value=0.0, value=20.0)
    C_abs = st.number_input("Capacidad máxima de absorción (L/kg)", value=4.0)
    eta = st.slider("Porcentaje de saturación efectiva (%)", 0, 100, 85) / 100
    V_rec = m_abs * C_abs * eta

if "Dispersantes" in metodos:
    aumento_diss = st.slider("Aumento estimado de disolución por dispersantes (%)", 0, 100, 20)
    factor_dispersante = 1 + aumento_diss / 100

# 3. Parámetros físicos
st.markdown("### 3. Parámetros físicos")
v_viento = st.slider("Velocidad del viento (m/s)", 0.0, 15.0, 5.0)
altura_ola = st.slider("Altura significativa de ola (m)", 0.0, 5.0, 1.5)
T_agua = st.slider("Temperatura del agua (°C)", 0, 30, 14)

# 4. Selección de hidrocarburo
st.markdown("### 4. Tipo de hidrocarburo")
tipos = {
    "Diésel": 0.05,
    "Crudo liviano": 0.02,
    "Crudo pesado": 0.01
}
tipo_hidrocarburo = st.selectbox("Seleccione el tipo de hidrocarburo derramado:", list(tipos.keys()))
k_bio = tipos[tipo_hidrocarburo]

# 5. Estimación de pérdidas físicas
st.markdown("### 5. Estimación de pérdidas físicas")
t_horas = t / 60
f_evap = 0.0001 * (v_viento ** 0.78) * (t_horas ** 0.5)
f_evap = min(f_evap, 0.9)
V_evap = V_d * f_evap

V_disperso = 0.02 * V_d * factor_dispersante
V_disu = 0.01 * V_d
V_bio = V_d * (1 - pow(2.71828, -k_bio * t_horas))

# 6. Remanente
V_rem = V_d - (V_skimmer + V_rec + V_evap + V_disperso + V_disu + V_bio)

# 7. Resultados y visualización
st.markdown("### 6. Resultados del balance de masa")
resultados = {
    "Skimmers": V_skimmer,
    "Absorbentes": V_rec,
    "Evaporado": V_evap,
    "Dispersado": V_disperso,
    "Disuelto": V_disu,
    "Biodegradado": V_bio,
    "Remanente": V_rem
}
df = pd.DataFrame.from_dict(resultados, orient='index', columns=["Volumen (L)"])
st.dataframe(df)

st.markdown("### 7. Visualización del Balance de Masa")
chart_type = st.radio("Seleccione el tipo de gráfico:", ["Torta", "Barplot", "Stacked Barplot"])

labels = list(resultados.keys())
values = list(resultados.values())

if chart_type == "Torta":
    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90, textprops={'fontsize': 10})
    ax.axis("equal")
    st.pyplot(fig)

elif chart_type == "Barplot":
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(labels, values)
    ax.set_ylabel("Volumen (L)")
    ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=9)
    ax.set_title("Distribución del Volumen", fontsize=12)
    st.pyplot(fig)

elif chart_type == "Stacked Barplot":
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(["Total"], [V_d], label="Total")
    bottom = 0
    for i in range(len(labels)):
        ax.bar(["Total"], [values[i]], bottom=bottom, label=labels[i])
        bottom += values[i]
    ax.set_ylabel("Volumen (L)")
    ax.set_title("Balance de Masa Apilado", fontsize=12)
    ax.legend()
    st.pyplot(fig)







