import streamlit as st
from datetime import datetime
import pdfkit
import tempfile
import os
import uuid

# --- Configuración inicial ---
st.set_page_config(page_title="Informe ETE Intraoperatoria", layout="centered")
st.title("🫀 Informe de Ecocardiografía Transesofágica Intraoperatoria")

# --- Asegurar carpeta para historial ---
os.makedirs("historial_informes", exist_ok=True)

# --- Formulario de datos del paciente ---
st.header("🧑‍⚕️ Datos del paciente")
with st.form(key="form_paciente"):
    col1, col2 = st.columns(2)
    with col1:
        nombre = st.text_input("Nombre completo")
        edad = st.number_input("Edad", min_value=0, max_value=120)
        sexo = st.selectbox("Sexo", ["Masculino", "Femenino"])
    with col2:
        historia = st.text_input("N° Historia Clínica")
        fecha = st.date_input("Fecha del estudio", value=datetime.today())
        cirugia = st.text_area("Tipo de cirugía", height=100)
    submitted_paciente = st.form_submit_button("Guardar datos del paciente")

# --- Guardar datos del paciente si se envían ---
if submitted_paciente:
    paciente_datos = {
        "nombre": nombre,
        "edad": edad,
        "sexo": sexo,
        "historia": historia,
        "fecha": fecha,
        "cirugia": cirugia
    }
    st.success("✅ Datos del paciente guardados correctamente.")

# --- Formulario del informe ecocardiográfico ---
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

    operador = st.text_input("Nombre del operador (firma digital)")
    submitted_eco = st.form_submit_button("Generar informe")

# --- Función para generar HTML ---
def generar_html(p, e, operador):
    hora = datetime.now().strftime("%H:%M:%S")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    html = f"""
    <h2>Informe de Ecocardiografía Transesofágica Intraoperatoria</h2>
    <p><strong>Paciente:</strong> {p['nombre']}<br>
    <strong>Edad:</strong> {p['edad']}<br>
    <strong>Sexo:</strong> {p['sexo']}<br>
    <strong>Historia Clínica:</strong> {p['historia']}<br>
    <strong>Fecha:</strong> {p['fecha'].strftime('%d-%m-%Y')}<br>
    <strong>Cirugía:</strong> {p['cirugia']}</p>
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

    html += f"<p><em>Informe generado por:</em> {operador}<br><em>Fecha y hora:</em> {timestamp}</p>"
    return html

# --- Procesamiento del informe ---
if submitted_eco and submitted_paciente and operador:
    datos_eco = {
        "lvef": lvef,
        "cavidades": cavidades,
        "valvulas": valvulas,
        "septo_iv": septo_iv,
        "funcion_diastolica": funcion_diastolica,
        "derrame": derrame,
        "gradiente_av": gradiente_av,
        "hallazgos": hallazgos
    }

    informe_html = generar_html(paciente_datos, datos_eco, operador)
    st.markdown(informe_html, unsafe_allow_html=True)

    # --- Mostrar como texto plano ---
    if st.button("📄 Mostrar informe como texto"):
        texto = informe_html.replace("<br>", "\n").replace("<li>", "- ").replace("</li>", "").replace("<ul>", "").replace("</ul>", "").replace("<p>", "").replace("</p>", "\n").replace("<em>", "").replace("</em>", "")
        st.text(texto)

    # --- Guardar como TXT en historial ---
    uid = uuid.uuid4().hex[:6]
    filename = f"historial_informes/Informe_{paciente_datos['nombre'].replace(' ', '_')}_{uid}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(texto)

    st.success(f"✅ Informe guardado localmente como `{filename}`")

    # --- Generar PDF y descargar ---
    if st.button("⬇️ Descargar PDF"):
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
                pdfkit.from_string(informe_html, tmp_pdf.name)
                with open(tmp_pdf.name, "rb") as f:
                    st.download_button("Descargar informe PDF", f, file_name="informe_ete.pdf", mime="application/pdf")
                os.unlink(tmp_pdf.name)
        except Exception as e:
            st.error(f"❌ Error al generar PDF: {e}")
