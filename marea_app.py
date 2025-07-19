import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
st.set_page_config(page_title="MAREA", layout="centered")
st.title("🌊 MAREA – Hydrocarbon Degradation Explorer")
st.subheader("Modelo de Análisis de Recuperación y Estimación de Absorción")
st.markdown("### 1. Datos del derrame")
Q = st.number_input("Caudal del derrame (L/min)", min_value=0.0, value=10.0)
t = st.number_input("Duración del derrame (min)", min_value=0.0, value=60.0)
V_d = Q * t
st.success(f"Volumen total derramado: {V_d:.1f} L")
st.markdown("### 2. Métodos utilizados")
metodos = st.multiselect(
    "Seleccione los métodos aplicados:",
    ["Barreras de contención", "Skimmers", "Absorbentes", "Dispersantes"]
)
V_skimmer = 0
V_rec = 0
factor_dispersante = 1.0
if "Skimmers" in metodos:
    V_skimmer = st.number_input("Volumen recuperado por skimmers (L)", min_value=0.0)
if "Absorbentes" in metodos:
    m_rec = st.number_input("Masa total del absorbente recuperado (kg)", min_value=0.0)
    m_abs = st.number_input("Masa seca del absorbente (kg)", min_value=0.0)
    C_abs = st.number_input("Capacidad máxima de absorción (L/kg)", value=4.0)
    eta = st.slider("Porcentaje de saturación efectiva (%)", 0, 100, 85) / 100
    V_rec = m_abs * C_abs * eta
if "Dispersantes" in metodos:
    aumento_diss = st.slider("Aumento estimado de disolución por dispersantes (%)", 0, 100, 20)
    factor_dispersante = 1 + aumento_diss / 100
st.markdown("### 3. Condiciones ambientales")
v_viento = st.slider("Velocidad del viento (m/s)", 0.0, 20.0, 5.0)
altura_ola = st.slider("Altura significativa de ola (m)", 0.0, 5.0, 1.5)
T_agua = st.slider("Temperatura del agua (°C)", 0, 30, 14)
st.markdown("### 4. Estimación de pérdidas físicas")
t_horas = t / 60
f_evap = 0.0001 * (v_viento ** 0.78) * (t_horas ** 0.5)
f_evap = min(f_evap, 0.9)
V_evap = V_d * f_evap
alpha = 0.01
f_disp = alpha * v_viento * altura_ola
f_disp = min(f_disp, 0.9)
V_disp = V_d * f_disp
kLa = 0.001  # 1/s
S = 0.02  # g/L
A = 100  # m²
V_diss = kLa * S * A * t * 60 * factor_dispersante
agua_en_aceite = 0.3
V_emul = V_d * (1 + agua_en_aceite)
st.markdown("### 5. Biodegradación")
tipo_hc = st.selectbox("Tipo de hidrocarburo:", ["Crudo liviano", "Crudo pesado", "Diésel marino", "Gasolina", "Lubricante usado", "BTEX"])
valores_k = {
    "Crudo liviano": 0.03,
    "Crudo pesado": 0.005,
    "Diésel marino": 0.035,
    "Gasolina": 0.045,
    "Lubricante usado": 0.002,
    "BTEX": 0.05
}
k_base = valores_k[tipo_hc]
theta = 1.07
T_ref = 20
k_bio = k_base * theta ** (T_agua - T_ref)
t_dias = st.slider("Días de simulación para biodegradación", 1, 60, 14)
V_total_recuperado = V_rec + V_skimmer
V_loss_fisico = V_evap + V_disp + V_diss
V_res = V_d - (V_total_recuperado + V_loss_fisico)
V_bio = V_res * (1 - np.exp(-k_bio * t_dias))
V_residual = V_res - V_bio
st.markdown("### 6. Resultados")
st.write(f"Volumen evaporado: {V_evap:.1f} L")
st.write(f"Volumen dispersado: {V_disp:.1f} L")
st.write(f"Volumen disuelto: {V_diss:.1f} L")
st.write(f"Volumen emulsificado (no pérdida): {V_emul:.1f} L")
st.write(f"Volumen biodegradado: {V_bio:.1f} L")
st.write(f"Volumen remanente no tratado: {V_residual:.1f} L")
st.markdown("## Balance de Masa del Hidrocarburo Derramado")
# ==========================
fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
    ax.axis("equal")
    st.pyplot(fig)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(labels, values, color="#6baed6")
    ax.set_title("Distribución del Volumen por Componente", fontsize=14)
    ax.set_ylabel("Volumen (L)")
    ax.set_xticklabels(labels, rotation=45, ha="right")
    st.pyplot(fig)
    eventos = ["Evento 1", "Evento 2"]
    valores_evento1 = values
    valores_evento2 = [v * 0.85 for v in values]
    bar_width = 0.5
    fig, ax = plt.subplots(figsize=(10, 6))
    bottom = [0] * len(eventos)
    for i, label in enumerate(labels):
        vals = [valores_evento1[i], valores_evento2[i]]
        ax.bar(eventos, vals, bar_width, label=label, bottom=bottom)
        bottom = [sum(x) for x in zip(bottom, vals)]
    ax.set_ylabel("Volumen (L)")
    ax.set_title("Comparación de Balance de Masa entre Eventos", fontsize=14)
    ax.legend(title="Componente", bbox_to_anchor=(1.05, 1), loc='upper left')
    st.pyplot(fig)
# ==========================
# 7. Visualización del Balance de Masa
# ==========================
st.subheader("7. Visualización del Balance de Masa")
chart_type = st.selectbox(
    "Selecciona el tipo de gráfico",
    ["Torta", "Barplot", "Stacked Barplot"]
)
labels = ["Absorbentes", "Skimmers", "Evaporado", "Dispersado", "Disuelto", "Biodegradado", "Remanente"]
values = [V_rec, V_skimmer, V_evap, V_disp, V_diss, V_bio, V_residual]
if chart_type == "Torta":
    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
    ax.axis("equal")
    st.pyplot(fig)
elif chart_type == "Barplot":
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(labels, values, color="#6baed6")
    ax.set_title("Distribución del Volumen por Componente", fontsize=14)
    ax.set_ylabel("Volumen (L)")
    ax.set_xticklabels(labels, rotation=45, ha="right")
    st.pyplot(fig)
elif chart_type == "Stacked Barplot":
    eventos = ["Evento 1", "Evento 2"]
    valores_evento1 = values
    valores_evento2 = [v * 0.85 for v in values]
    bar_width = 0.5
    fig, ax = plt.subplots(figsize=(10, 6))
    bottom = [0] * len(eventos)
    for i, label in enumerate(labels):
        vals = [valores_evento1[i], valores_evento2[i]]
        ax.bar(eventos, vals, bar_width, label=label, bottom=bottom)
        bottom = [sum(x) for x in zip(bottom, vals)]
    ax.set_ylabel("Volumen (L)")
    ax.set_title("Comparación de Balance de Masa entre Eventos", fontsize=14)
    ax.legend(title="Componente", bbox_to_anchor=(1.05, 1), loc='upper left')
    st.pyplot(fig)







