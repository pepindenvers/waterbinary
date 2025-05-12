import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image
import base64

st.set_page_config(page_title="Simulador Destilación Etanol-Agua", layout="centered")

# Cargar base de datos desde CSV
@st.cache_data
def cargar_datos():
    df = pd.read_csv("BINARIA.csv")
    return df

df = cargar_datos()

st.title("🧪 Simulador de Destilación Etanol-Agua")
st.write("Simulador interactivo para la destilación de mezclas etanol-agua usando datos reales de índice de refracción y fracciones molares.")

# Paso 1: Selección de concentración
porc_inicial = st.slider("Selecciona el porcentaje de etanol inicial en la mezcla", 0, 100, step=2)

if 'etapas' not in st.session_state:
    st.session_state.etapas = []

if st.button("Iniciar medición"):
    file_ = open("alcoho.gif", "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()
    st.markdown(
        f'<img src="data:image/gif;base64,{data_url}" alt="mezcla" style="width: 300px;">',
        unsafe_allow_html=True,
    )
    st.session_state.etapas.append(porc_inicial)

# Mostrar datos medidos
if st.session_state.etapas:
    if st.button("Continuar medición"):
        mediciones = df[df["Etanol porcentaje"] == porc_inicial]
        if not mediciones.empty:
            st.success("Índice de refracción encontrado:")
            st.write(mediciones[["indice de refraccion"]])
        else:
            st.error("Datos no encontrados para ese porcentaje.")
    if st.button("Finalizar"):
        st.subheader("📈 Gráfica de Calibración")
        fig, ax = plt.subplots()
        ax.plot(df["Etanol porcentaje"], df["indice de refraccion"], marker="o")
        ax.set_xlabel("Porcentaje de Etanol (%)")
        ax.set_ylabel("Índice de Refracción")
        ax.set_title("Curva de Calibración")
        st.pyplot(fig)

        if st.button("Destilar"):
            # Mostrar GIF de destilación
            file_ = open("destila.gif", "rb")
            contents = file_.read()
            data_url = base64.b64encode(contents).decode("utf-8")
            file_.close()
            st.markdown(
                f'<img src="data:image/gif;base64,{data_url}" alt="destilacion" style="width: 300px;">',
                unsafe_allow_html=True,
            )

            # Solicitar al usuario seleccionar la temperatura
            temperatura_seleccionada = st.selectbox(
                "Selecciona la temperatura de ebullición",
                [78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 100]
            )

            # Buscar los índices de refracción para la temperatura seleccionada
            datos_destilacion = df[df["EBULLICION TEMPERATURA"] == temperatura_seleccionada]

            if not datos_destilacion.empty:
                ndl = datos_destilacion["indice de refraccion"].values[0]  # Índice de refracción líquido
                ndv = datos_destilacion["nd indice de refraccion"].values[0]  # Índice de refracción vapor

                st.write(f"📌 **Índice de refracción (líquido) a {temperatura_seleccionada}°C:** {ndl}")
                st.write(f"📌 **Índice de refracción (vapor) a {temperatura_seleccionada}°C:** {ndv}")
            else:
                st.warning(f"No se encontraron datos para la temperatura {temperatura_seleccionada}°C.")
