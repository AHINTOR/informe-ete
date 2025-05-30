import streamlit as st
from datetime import datetime
import pdfkit
import tempfile
import os

st.set_page_config(page_title="Informe ETE Intraoperatoria", layout="centered")
st.title("🫀 Informe de Ecocardiografía Transesofágica Intraoperatoria")

# --- Inicializar variables ---
paciente_datos = {}
eco_datos = {}

# --- Sección 1: Datos del paciente ---
st.header("🧑‍⚕️ Datos del paciente")

with st.form(key="form_paciente"):
    col1, col2 = st.columns(2)
    with col1:
        nombre = st.text_input("Nombre completo")
        edad = st.number_input("Edad", min_value=0, max_value=120, step=1)
        sexo = st.selectbox("Sexo", ["Masculino", "Femenino"])
    with col2:
        historia = st.text_input("N° Historia Clínica")
        fecha = st.date_input("Fecha del estudio", value=datetime.today())
        cirugia = st.text_area("Tipo de cirugía", height=100)
    submitted_paciente = st.form_submit_button("Guardar datos del paciente")

if submitted_paciente:
    paciente_datos = {
        "nombre": nombre,
        "edad": edad,
        "sexo": sexo,
        "historia": historia,
        "fecha": fecha,
        "cirugia": cirugia
    }
    st.success("✅ Datos del paciente guardados")

# --- Sección 2: Informe ecocardiográfico ---
st.header("📋 Datos ecocardiográficos")

with st.form(key="form_eco"):
    lvef = st.select_slider("Fracción de eyección (LVEF)", options=["<30%", "30-40%", "40-50%", "50-60%", ">60%"])
    cavidades = st.text_area("Tamaño y función de cavidades", height=100)
    valvulas = st.text_area("Evaluación valvular", height=100)
    septo_iv = st.text_area("Septo interventricular", height=100)
    funcion_diastolica = st.text_area("Función diastólica", height=100)
    derrame = st.selectbox("Derrame pericárdico", ["No", "Leve", "Moderado", "Severo"])
    gradiente_av = st.text_input("Gradiente AV (mmHg)")

    hallazgos = st.multiselect(
        "Hallazgos adicionales:",
        ["CIA tipo ostium secundum", "CIV membranosa", "Insuficiencia mitral severa",
         "Trombo auricular izquierdo", "Derrame pericárdico severo"]
    )

    submitted_eco = st.form_submit_button("Generar informe")

# --- Generar informe HTML ---
def generar_html(p, e):
    html = f"""
    <h2>Informe Ecocardiografía Transesofágica Intraoperatoria</h2>
    <p><strong>Paciente:</strong> {p['nombre']}<br>
    <strong>Edad:</strong> {p['edad']}<br>
    <strong>Sexo:</strong> {p['sexo']}<br>
    <strong>Historia Clínica:</strong> {p['historia']}<br>
    <strong>Fecha:</strong> {p['fecha'].strftime("%d-%m-%Y")}<br>
    <strong>Tipo de cirugía:</strong> {p['cirugia']}</p>
    <hr>
    <h3>Resumen ecocardiográfico</h3>
    <ul>
        <li><strong>LVEF:</strong> {e['lvef']}</li>
        <li><strong>Cavidades:</strong> {e['cavidades']}</li>
        <li><strong>Valvulopatías:</strong> {e['valvulas']}</li>
        <li><strong>Septo IV:</strong> {e['septo_iv']}</li>
        <li><strong>Función diastólica:</strong> {e['funcion_diastolica']}</li>
        <li><strong>Derrame pericárdico:</strong> {e['derrame']}</li>
        <li><strong>Gradiente AV:</strong> {e['gradiente_av']} mmHg</li>
    </ul>
    """
    if e["hallazgos"]:
        html += "<h4>Hallazgos adicionales:</h4><ul>"
        for h in e["hallazgos"]:
            html += f"<li>{h}</li>"
        html += "</ul>"
    return html

# --- Mostrar informe si se generó ---
if submitted_eco and paciente_datos:
    eco_datos = {
        "lvef": lvef,
        "cavidades": cavidades,
        "valvulas": valvulas,
        "septo_iv": septo_iv,
        "funcion_diastolica": funcion_diastolica,
        "derrame": derrame,
        "gradiente_av": gradiente_av,
        "hallazgos": hallazgos
    }

    st.success("✅ Informe generado correctamente")
    informe_html = generar_html(paciente_datos, eco_datos)
    st.markdown(informe_html, unsafe_allow_html=True)

    if st.button("📄 Mostrar informe como texto"):
        informe_txt = (
            f"Informe ETE Intraoperatoria\n"
            f"Paciente: {paciente_datos['nombre']}\nEdad: {paciente_datos['edad']}\n"
            f"Sexo: {paciente_datos['sexo']}\nHistoria Clínica: {paciente_datos['historia']}\n"
            f"Fecha: {paciente_datos['fecha'].strftime('%d-%m-%Y')}\nCirugía: {paciente_datos['cirugia']}\n\n"
            f"LVEF: {eco_datos['lvef']}\nCavidades: {eco_datos['cavidades']}\nValvulopatías: {eco_datos['valvulas']}\n"
            f"Septo IV: {eco_datos['septo_iv']}\nFunción diastólica: {eco_datos['funcion_diastolica']}\n"
            f"Derrame: {eco_datos['derrame']}\nGradiente AV: {eco_datos['gradiente_av']} mmHg\n"
            f"Hallazgos: {', '.join(eco_datos['hallazgos']) if eco_datos['hallazgos'] else 'Ninguno'}"
        )
        st.text(informe_txt)

    if st.button("⬇️ Descargar PDF"):
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
                pdfkit.from_string(informe_html, tmp_pdf.name)
                with open(tmp_pdf.name, "rb") as f:
                    st.download_button("Descargar informe PDF", f, file_name="informe_ete.pdf", mime="application/pdf")
                os.unlink(tmp_pdf.name)
        except Exception as e:
            st.error(f"❌ Error al generar PDF: {e}")
