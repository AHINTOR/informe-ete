import streamlit as st
from datetime import datetime
import pdfkit
import tempfile
import os

st.set_page_config(page_title="Informe ETE Intraoperatoria", layout="centered")
st.title("🫀 Informe de Ecocardiografía Transesofágica Intraoperatoria")

# --- Sección 1: Datos del paciente ---
st.header("🧑‍⚕️ Datos del paciente")

with st.form("datos_paciente"):
    col1, col2 = st.columns(2)
    with col1:
        nombre = st.text_input("Nombre completo")
        edad = st.number_input("Edad", min_value=0, max_value=120, step=1)
        sexo = st.selectbox("Sexo", ["Masculino", "Femenino"])
    with col2:
        historia = st.text_input("N° Historia Clínica")
        fecha = st.date_input("Fecha del estudio", value=datetime.today())
        cirugia = st.text_area("Tipo de cirugía", height=80)  # altura mínima permitida
    submitted_1 = st.form_submit_button("Guardar datos del paciente")

# --- Sección 2: Informe ecocardiográfico ---
st.header("📋 Datos ecocardiográficos")

with st.form("datos_eco"):
    lvef = st.select_slider("Fracción de eyección (LVEF)", options=["<30%", "30-40%", "40-50%", "50-60%", ">60%"])
    cavidades = st.text_area("Tamaño y función de cavidades", height=100)
    valvulas = st.text_area("Evaluación valvular", height=100)
    septo_iv = st.text_area("Septo interventricular", height=80)
    funcion_diastolica = st.text_area("Función diastólica", height=80)
    derrame = st.selectbox("Derrame pericárdico", ["No", "Leve", "Moderado", "Severo"])
    gradiente_av = st.text_input("Gradiente AV (mmHg)")

    hallazgos = st.multiselect(
        "Hallazgos adicionales:",
        ["CIA tipo ostium secundum", "CIV membranosa", "Insuficiencia mitral severa",
         "Trombo auricular izquierdo", "Derrame pericárdico severo"]
    )

    informe_generado = st.form_submit_button("Generar informe")

# --- Generar informe HTML ---
def generar_html():
    html = f"""
    <h2>Informe Ecocardiografía Transesofágica Intraoperatoria</h2>
    <p><strong>Paciente:</strong> {nombre}<br>
    <strong>Edad:</strong> {edad}<br>
    <strong>Sexo:</strong> {sexo}<br>
    <strong>Historia Clínica:</strong> {historia}<br>
    <strong>Fecha:</strong> {fecha.strftime("%d-%m-%Y")}<br>
    <strong>Tipo de cirugía:</strong> {cirugia}</p>
    <hr>
    <h3>Resumen ecocardiográfico</h
