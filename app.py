import streamlit as st
from datetime import datetime
import pdfkit
import tempfile
import os
import uuid

st.set_page_config(page_title="Informe ETE Intraoperatoria", layout="centered")
st.title("🫀 Informe de Ecocardiografía Transesofágica Intraoperatoria")

# Asegurar carpeta local para guardar historial de informes
os.makedirs("historial_informes", exist_ok=True)

paciente_datos = {}
datos_eco = {}

# --- FORMULARIO: Datos del paciente ---
with st.form("form_paciente"):
    st.subheader("🧑‍⚕️ Datos del paciente")
    col1, col2 = st.columns(2)
    with col1:
        nombre = st.text_input("Nombre completo")
        edad = st.number_input("Edad", min_value=0, max_value=120)
        sexo = st.selectbox("Sexo", ["Masculino", "Femenino"])
    with col2:
        historia = st.text_input("N° Historia Clínica")
        fecha = st.date_input("Fecha del estudio", value=datetime.today())
        cirugia = st.text_area("Tipo de cirugía", height=100)

    operador = st.text_input("Nombre del operador (firma digital)")
    submit_paciente = st.form_submit_button("✅ Continuar con datos ecocardiográficos")

# --- FORMULARIO: Datos ecocardiográficos ---
if submit_paciente:
    paciente_datos = {
        "nombre": nombre,
        "edad": edad,
        "sexo": sexo,
        "historia": historia,
        "fecha": fecha,
        "cirugia": cirugia,
        "operador": operador
    }

    with st.form("form_eco"):
        st.subheader("📋 Informe ecocardiográfico")
        lvef = st.select_slider("Fracción de eyección (LVEF)", options=["<30%", "30-40%", "40-50%", "50-60%", ">60%"])
        cavidades = st.text_area("Tamaño y función de cavidades", height=100)
        valvulas = st.text_area("Evaluación valvular", height=100)
        septo_iv = st.text_area("Septo interventricular", height=100)
        funcion_diastolica = st.text_area("Función diastólica", height=100)
        derrame = st.selectbox("Derrame pericárdico", ["No", "Leve", "Moderado", "Severo"])
        gradiente_av = st.text_input("Gradiente AV (mmHg)")

        hallazgos = st.multiselect(
            "Hallazgos adicionales",
            ["CIA tipo ostium secundum", "CIV membranosa", "Insuficiencia mitral severa",
             "Trombo auricular izquierdo", "Derrame pericárdico severo"]
        )

        generar_informe = st.form_submit_button("📝 Generar informe")

# --- Generador HTML del informe ---
def generar_html(p, e):
    html = f"""
    <h2>Informe de Ecocardiografía Transesofágica Intraoperatoria</h2>
    <p><strong>Paciente:</strong> {p['nombre']}<br>
    <strong>Edad:</strong> {p['edad']}<br>
    <strong>Sexo:</strong> {p['sexo']}<br>
    <strong>Historia Clínica:</strong> {p['historia']}<br>
    <strong>Fecha del estudio:</strong> {p['fecha'].strftime('%d-%m-%Y')}<br>
    <strong>Cirugía:</strong> {p['cirugia']}</p>
    <hr>
    <ul>
        <li><strong>LVEF:</strong> {e['lvef']}</li>
        <li><strong>Cavidades:</strong> {e['cavidades']}</li>
        <li><strong>Valvulopatías:</strong> {e['valvulas']}</li>
        <li><strong>Septo IV:</strong> {e['septo_iv']}</li>
        <li><strong>Función diastólica:</strong> {e['funcion_diastolica']}</li>
        <li><strong>Derrame:</strong> {e['derrame']}</li>
        <li><strong>Gradiente AV:</strong> {e['gradiente_av']} mmHg</li>
    </ul>
    """
    if e["hallazgos"]:
        html += "<h4>Hallazgos adicionales:</h4><ul>"
        for h in e["hallazgos"]:
            html += f"<li>{h}</li>"
        html += "</ul>"

    html += f"<p><em>Operador:</em> {p['operador']}<br><em>Generado:</em> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>"
    return html

# --- Mostrar informe y botones ---
if 'generar_informe' in locals() and generar_informe:
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

    informe_html = generar_html(paciente_datos, datos_eco)
    informe_txt = informe_html.replace("<br>", "\n").replace("<li>", "- ").replace("</li>", "").replace("<ul>", "").replace("</ul>", "").replace("<p>", "").replace("</p>", "\n").replace("<em>", "").replace("</em>", "")

    st.markdown(informe_html, unsafe_allow_html=True)

    # Guardar como historial en .txt
    uid = uuid.uuid4().hex[:6]
    filename = f"historial_informes/informe_{paciente_datos['nombre'].replace(' ', '_')}_{uid}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(informe_txt)

    st.success(f"✅ Informe guardado como: `{filename}`")

    # Mostrar como texto
    if st.button("📄 Mostrar informe como texto plano"):
        st.text(informe_txt)

    # Descargar como PDF
    if st.button("⬇️ Descargar informe en PDF"):
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
                pdfkit.from_string(informe_html, tmp_pdf.name)
                with open(tmp_pdf.name, "rb") as f:
                    st.download_button("Descargar PDF", f, file_name="informe_ecocardio.pdf", mime="application/pdf")
                os.unlink(tmp_pdf.name)
        except Exception as e:
            st.error(f"❌ Error al generar PDF: {e}")
