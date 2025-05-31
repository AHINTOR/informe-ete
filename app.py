import streamlit as st
from datetime import datetime, date
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import io
import base64

# Configuración de la página
st.set_page_config(
    page_title="Informe Ecocardiografía Transesofágica",
    page_icon="🫀",
    layout="wide"
)

def generate_pdf(report_text, patient_name):
    """Genera un PDF del informe"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Estilo personalizado para el título
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    # Estilo para el contenido
    content_style = ParagraphStyle(
        'CustomContent',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=12,
        alignment=TA_LEFT
    )
    
    # Construir el documento
    story = []
    story.append(Paragraph("INFORME DE ECOCARDIOGRAFÍA TRANSESOFÁGICA INTRAOPERATORIA", title_style))
    story.append(Spacer(1, 20))
    
    # Dividir el texto en párrafos y agregar al PDF
    paragraphs = report_text.split('\n')
    for para in paragraphs:
        if para.strip():
            story.append(Paragraph(para, content_style))
        else:
            story.append(Spacer(1, 12))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

def create_download_link(pdf_buffer, filename):
    """Crea un enlace de descarga para el PDF"""
    b64 = base64.b64encode(pdf_buffer.read()).decode()
    href = f'<a href="data:application/pdf;base64,{b64}" download="{filename}">📥 Descargar Informe PDF</a>'
    return href

# Título principal
st.title("🫀 Informe de Ecocardiografía Transesofágica Intraoperatoria")
st.markdown("---")

# Sidebar para navegación
st.sidebar.title("Navegación")
section = st.sidebar.selectbox(
    "Seleccionar sección:",
    ["Datos del Paciente", "Datos del Estudio", "Hallazgos Ecocardiográficos", "Informe Final"]
)

# Inicializar session state
if 'patient_data' not in st.session_state:
    st.session_state.patient_data = {}
if 'study_data' not in st.session_state:
    st.session_state.study_data = {}
if 'echo_findings' not in st.session_state:
    st.session_state.echo_findings = {}

# SECCIÓN 1: DATOS DEL PACIENTE
if section == "Datos del Paciente":
    st.header("📋 Datos del Paciente")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.session_state.patient_data['nombre'] = st.text_input("Nombre completo", value=st.session_state.patient_data.get('nombre', ''))
        st.session_state.patient_data['edad'] = st.number_input("Edad", min_value=0, max_value=120, value=st.session_state.patient_data.get('edad', 0))
        st.session_state.patient_data['sexo'] = st.selectbox("Sexo", ["Masculino", "Femenino"], index=0 if st.session_state.patient_data.get('sexo') == "Masculino" else 1)
        st.session_state.patient_data['peso'] = st.number_input("Peso (kg)", min_value=0.0, value=st.session_state.patient_data.get('peso', 0.0), format="%.1f")
    
    with col2:
        st.session_state.patient_data['historia'] = st.text_input("N° Historia Clínica", value=st.session_state.patient_data.get('historia', ''))
        st.session_state.patient_data['talla'] = st.number_input("Talla (cm)", min_value=0.0, value=st.session_state.patient_data.get('talla', 0.0), format="%.1f")
        st.session_state.patient_data['superficie_corporal'] = st.number_input("Superficie corporal (m²)", min_value=0.0, value=st.session_state.patient_data.get('superficie_corporal', 0.0), format="%.2f")
    
    st.session_state.patient_data['diagnostico_preop'] = st.text_area("Diagnóstico preoperatorio", value=st.session_state.patient_data.get('diagnostico_preop', ''))

# SECCIÓN 2: DATOS DEL ESTUDIO
elif section == "Datos del Estudio":
    st.header("🏥 Datos del Estudio")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.session_state.study_data['fecha'] = st.date_input("Fecha del estudio", value=st.session_state.study_data.get('fecha', date.today()))
        st.session_state.study_data['hora'] = st.time_input("Hora del estudio", value=st.session_state.study_data.get('hora', datetime.now().time()))
        st.session_state.study_data['medico'] = st.text_input("Médico responsable", value=st.session_state.study_data.get('medico', ''))
    
    with col2:
        st.session_state.study_data['institucion'] = st.text_input("Institución", value=st.session_state.study_data.get('institucion', ''))
        st.session_state.study_data['equipo'] = st.text_input("Equipo utilizado", value=st.session_state.study_data.get('equipo', ''))
        st.session_state.study_data['sonda'] = st.text_input("Sonda utilizada", value=st.session_state.study_data.get('sonda', ''))
    
    st.session_state.study_data['indicacion'] = st.text_area("Indicación del estudio", value=st.session_state.study_data.get('indicacion', ''))

# SECCIÓN 3: HALLAZGOS ECOCARDIOGRÁFICOS
elif section == "Hallazgos Ecocardiográficos":
    st.header("🔍 Hallazgos Ecocardiográficos")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Función Ventricular", "Válvulas", "Otras Estructuras", "Hallazgos Adicionales"])
    
    with tab1:
        st.subheader("Función Ventricular Izquierda")
        col1, col2 = st.columns(2)
        
        with col1:
            st.session_state.echo_findings['fevi'] = st.selectbox(
                "Fracción de eyección VI",
                ["Normal (>55%)", "Levemente reducida (45-55%)", "Moderadamente reducida (30-44%)", "Severamente reducida (<30%)"],
                index=0
            )
            st.session_state.echo_findings['contractilidad'] = st.selectbox(
                "Contractilidad global",
                ["Normal", "Hipocinesia leve", "Hipocinesia moderada", "Hipocinesia severa", "Acinesia", "Discinesia"],
                index=0
            )
        
        with col2:
            st.session_state.echo_findings['alteraciones_segmentarias'] = st.text_area("Alteraciones segmentarias", value=st.session_state.echo_findings.get('alteraciones_segmentarias', ''))
        
        st.subheader("Función Ventricular Derecha")
        st.session_state.echo_findings['funcion_vd'] = st.selectbox(
            "Función VD",
            ["Normal", "Levemente deprimida", "Moderadamente deprimida", "Severamente deprimida"],
            index=0
        )
    
    with tab2:
        st.subheader("Válvulas")
        
        # Válvula Mitral
        st.write("**Válvula Mitral**")
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.echo_findings['mitral_insuficiencia'] = st.selectbox(
                "Insuficiencia mitral",
                ["Ausente", "Trivial", "Leve", "Moderada", "Severa"],
                index=0
            )
        with col2:
            st.session_state.echo_findings['mitral_estenosis'] = st.selectbox(
                "Estenosis mitral",
                ["Ausente", "Leve", "Moderada", "Severa"],
                index=0
            )
        
        # Válvula Aórtica
        st.write("**Válvula Aórtica**")
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.echo_findings['aortica_insuficiencia'] = st.selectbox(
                "Insuficiencia aórtica",
                ["Ausente", "Trivial", "Leve", "Moderada", "Severa"],
                index=0
            )
        with col2:
            st.session_state.echo_findings['aortica_estenosis'] = st.selectbox(
                "Estenosis aórtica",
                ["Ausente", "Leve", "Moderada", "Severa"],
                index=0
            )
        
        # Válvula Tricúspide
        st.write("**Válvula Tricúspide**")
        st.session_state.echo_findings['tricuspide_insuficiencia'] = st.selectbox(
            "Insuficiencia tricúspide",
            ["Ausente", "Trivial", "Leve", "Moderada", "Severa"],
            index=0
        )
        
        # Válvula Pulmonar
        st.write("**Válvula Pulmonar**")
        st.session_state.echo_findings['pulmonar'] = st.text_input("Válvula pulmonar", value=st.session_state.echo_findings.get('pulmonar', 'Normal'))
    
    with tab3:
        st.subheader("Otras Estructuras")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.session_state.echo_findings['septum_interauricular'] = st.text_input("Septum interauricular", value=st.session_state.echo_findings.get('septum_interauricular', 'Íntegro'))
            st.session_state.echo_findings['septum_interventricular'] = st.text_input("Septum interventricular", value=st.session_state.echo_findings.get('septum_interventricular', 'Íntegro'))
            st.session_state.echo_findings['pericardio'] = st.text_input("Pericardio", value=st.session_state.echo_findings.get('pericardio', 'Sin alteraciones'))
        
        with col2:
            st.session_state.echo_findings['aorta'] = st.text_input("Aorta", value=st.session_state.echo_findings.get('aorta', 'Normal'))
            st.session_state.echo_findings['auricula_izq'] = st.text_input("Aurícula izquierda", value=st.session_state.echo_findings.get('auricula_izq', 'Tamaño normal'))
            st.session_state.echo_findings['venas_pulmonares'] = st.text_input("Venas pulmonares", value=st.session_state.echo_findings.get('venas_pulmonares', 'Normales'))
    
    with tab4:
        st.subheader("Hallazgos Adicionales")
        st.session_state.echo_findings['otros_hallazgos'] = st.text_area(
            "Otros hallazgos",
            value=st.session_state.echo_findings.get('otros_hallazgos', ''),
            height=150
        )
        st.session_state.echo_findings['conclusiones'] = st.text_area(
            "Conclusiones",
            value=st.session_state.echo_findings.get('conclusiones', ''),
            height=150
        )

# SECCIÓN 4: INFORME FINAL
elif section == "Informe Final":
    st.header("📄 Informe Final")
    
    # Generar el informe
    report = f"""INFORME DE ECOCARDIOGRAFÍA TRANSESOFÁGICA INTRAOPERATORIA

DATOS DEL PACIENTE:
Nombre: {st.session_state.patient_data.get('nombre', 'No especificado')}
Edad: {st.session_state.patient_data.get('edad', 'No especificada')} años
Sexo: {st.session_state.patient_data.get('sexo', 'No especificado')}
Historia Clínica: {st.session_state.patient_data.get('historia', 'No especificada')}
Peso: {st.session_state.patient_data.get('peso', 'No especificado')} kg
Talla: {st.session_state.patient_data.get('talla', 'No especificada')} cm
Superficie corporal: {st.session_state.patient_data.get('superficie_corporal', 'No especificada')} m²

DIAGNÓSTICO PREOPERATORIO:
{st.session_state.patient_data.get('diagnostico_preop', 'No especificado')}

DATOS DEL ESTUDIO:
Fecha: {st.session_state.study_data.get('fecha', 'No especificada')}
Hora: {st.session_state.study_data.get('hora', 'No especificada')}
Institución: {st.session_state.study_data.get('institucion', 'No especificada')}
Médico responsable: {st.session_state.study_data.get('medico', 'No especificado')}
Equipo utilizado: {st.session_state.study_data.get('equipo', 'No especificado')}
Sonda utilizada: {st.session_state.study_data.get('sonda', 'No especificada')}

INDICACIÓN:
{st.session_state.study_data.get('indicacion', 'No especificada')}

HALLAZGOS ECOCARDIOGRÁFICOS:

FUNCIÓN VENTRICULAR:
- Función ventricular izquierda: {st.session_state.echo_findings.get('fevi', 'No evaluada')}
- Contractilidad global: {st.session_state.echo_findings.get('contractilidad', 'No evaluada')}
- Función ventricular derecha: {st.session_state.echo_findings.get('funcion_vd', 'No evaluada')}
- Alteraciones segmentarias: {st.session_state.echo_findings.get('alteraciones_segmentarias', 'No descriptas')}

VÁLVULAS:
- Válvula mitral: Insuficiencia {st.session_state.echo_findings.get('mitral_insuficiencia', 'no evaluada')}, Estenosis {st.session_state.echo_findings.get('mitral_estenosis', 'no evaluada')}
- Válvula aórtica: Insuficiencia {st.session_state.echo_findings.get('aortica_insuficiencia', 'no evaluada')}, Estenosis {st.session_state.echo_findings.get('aortica_estenosis', 'no evaluada')}
- Válvula tricúspide: Insuficiencia {st.session_state.echo_findings.get('tricuspide_insuficiencia', 'no evaluada')}
- Válvula pulmonar: {st.session_state.echo_findings.get('pulmonar', 'No evaluada')}

OTRAS ESTRUCTURAS:
- Septum interauricular: {st.session_state.echo_findings.get('septum_interauricular', 'No evaluado')}
- Septum interventricular: {st.session_state.echo_findings.get('septum_interventricular', 'No evaluado')}
- Aorta: {st.session_state.echo_findings.get('aorta', 'No evaluada')}
- Aurícula izquierda: {st.session_state.echo_findings.get('auricula_izq', 'No evaluada')}
- Venas pulmonares: {st.session_state.echo_findings.get('venas_pulmonares', 'No evaluadas')}
- Pericardio: {st.session_state.echo_findings.get('pericardio', 'No evaluado')}

OTROS HALLAZGOS:
{st.session_state.echo_findings.get('otros_hallazgos', 'No descriptos')}

CONCLUSIONES:
{st.session_state.echo_findings.get('conclusiones', 'No especificadas')}

Fecha del informe: {datetime.now().strftime('%d/%m/%Y %H:%M')}
Médico informante: {st.session_state.study_data.get('medico', 'No especificado')}
"""
    
    # Mostrar el informe
    st.text_area("Informe generado:", value=report, height=600)
    
    # Botones de acción
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Regenerar Informe"):
            st.rerun()
    
    with col2:
        if st.button("📋 Copiar al Portapapeles"):
            st.write("Copia el texto del área de arriba")
    
    with col3:
        # Generar y descargar PDF
        if st.button("📥 Generar PDF"):
            if st.session_state.patient_data.get('nombre'):
                pdf_buffer = generate_pdf(report, st.session_state.patient_data['nombre'])
                filename = f"ETE_Informe_{st.session_state.patient_data['nombre'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf"
                
                st.download_button(
                    label="📥 Descargar PDF",
                    data=pdf_buffer.getvalue(),
                    file_name=filename,
                    mime="application/pdf"
                )
            else:
                st.error("Por favor, ingrese el nombre del paciente en la sección 'Datos del Paciente'")

# Footer
st.markdown("---")
st.markdown("*Aplicación para generación de informes de ecocardiografía transesofágica intraoperatoria*")
