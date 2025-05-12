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
    df.columns = df.columns.str.strip()  # Eliminar espacios extras de las columnas
    return df

df = cargar_datos()

# Verificar las columnas del DataFrame para asegurarnos de que "X (líquido)" existe
st.write("Columnas disponibles en el archivo CSV:", df.columns)

st.title("🧪 Simulador de Destilación Etanol-Agua")
st.write("Simulador interactivo para la destilación de mezclas etanol-agua usando datos reales de índice de refracción y fracciones molares.")

# Paso 1: Selección de concentración
porc_inicial = st.slider("Selecciona el porcentaje de etanol inicial en la mezcla", 0, 100, step=2)

if 'etapas' not in st.session_state:
    st.session_state.etapas = []

# Botón para iniciar medición
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

# Ahora el botón Destilar al final
destilar_button = st.button("Destilar")

if destilar_button:
    # Mostrar el gif de destilación
    file_ = open("destila.gif", "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()
    st.markdown(
        f'<img src="data:image/gif;base64,{data_url}" alt="destilacion" style="width: 300px;">',
        unsafe_allow_html=True,
    )

    # Pedir la temperatura de ebullición
    temperaturas_disponibles = [78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 100]

    temperatura_seleccionada = st.selectbox(
        "Selecciona la temperatura de ebullición",
        temperaturas_disponibles,
        index=temperaturas_disponibles.index(78)  # Establece 78 como temperatura predeterminada
    )

    # Verificar si la temperatura seleccionada está en el DataFrame
    if "Ebullicion" not in df.columns:
        st.error("Error: La columna 'Ebullicion' no existe en el archivo CSV.")
    else:
        # Asegurarnos de que la temperatura seleccionada esté en el DataFrame
        if temperatura_seleccionada in df["Ebullicion"].values:
            datos_destilacion = df[df["Ebullicion"] == temperatura_seleccionada]

            # Verificar si las columnas 'ndl' y 'ndv' existen en el DataFrame
            if "ndl" not in df.columns or "ndv" not in df.columns:
                st.error("Error: Las columnas 'ndl' o 'ndv' no existen en el archivo CSV.")
            else:
                if not datos_destilacion.empty:
                    # Mostrar los resultados de ndl (líquido) y ndv (vapor)
                    X_etoh = datos_destilacion["ndl"].values[0]
                    Y_etoh = datos_destilacion["ndv"].values[0]
                    st.write(f"Temperatura de ebullición seleccionada: {temperatura_seleccionada}°C")
                    st.write(f"Fracción molar de etanol en la fase líquida (X): {X_etoh}")
                    st.write(f"Fracción molar de etanol en la fase vapor (Y): {Y_etoh}")
                else:
                    st.error("No se encontraron datos para la temperatura seleccionada en el CSV.")
        else:
            st.error("La temperatura seleccionada no está disponible en los datos.")




