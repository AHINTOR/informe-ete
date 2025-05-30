import streamlit as st
from datetime import datetime

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
        cirugia = st.text_area("Tipo de cirugía", height=60)
    
    st.form_submit_button("Guardar datos del paciente")

# --- Sección 2: Datos ecocardiográficos básicos ---
st.header("📋 Datos ecocardiográficos")

with st.form("datos_eco"):
    lvef = st.select_slider("Fracción de eyección (LVEF)", options=["<30%", "30-40%", "40-50%", "50-60%", ">60%"])
    cavidades = st.text_area("Tamaño y función de cavidades", height=100)
    valvulas = st.text_area("Evaluación valvular", height=100)
    septo_iv = st.text_area("Evaluación del septo interventricular", height=80)
    derrame = st.selectbox("Derrame pericárdico", ["No", "Leve", "Moderado", "Severo"])
    gradiente_av = st.text_input("Gradiente transvalvular AV (mmHg)")

    informe_generado = st.form_submit_button("Generar informe")

# --- Sección 3: Visualización del informe generado ---
if informe_generado:
    st.success("✅ Informe generado:")
    st.markdown(f"""
    **Paciente:** {nombre}  
    **Edad:** {edad}  
    **Sexo:** {sexo}  
    **Historia Clínica:** {historia}  
    **Fecha del estudio:** {fecha.strftime("%d-%m-%Y")}  
    **Cirugía:** {cirugia}  
    
    ---

    ### Informe Ecocardiográfico

    - **Fracción de eyección (LVEF):** {lvef}  
    - **Cavidades:**  
      {cavidades}  
    - **Evaluación valvular:**  
      {valvulas}  
    - **Septo interventricular:**  
      {septo_iv}  
    - **Derrame pericárdico:** {derrame}  
    - **Gradiente AV:** {gradiente_av} mmHg
    """)

    st.download_button(
        label="📄 Descargar informe en TXT",
        data=f"Informe Ecocardiografía\n\nPaciente: {nombre}\nEdad: {edad}\nSexo: {sexo}\n...",
        file_name="informe_eco.txt",
        mime="text/plain"
    )
