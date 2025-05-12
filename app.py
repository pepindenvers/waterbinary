import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
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

        # Mostrar gif de destilación
        file_ = open("destila.gif", "rb")
        contents = file_.read()
        data_url = base64.b64encode(contents).decode("utf-8")
        file_.close()
        st.markdown(
            f'<img src="data:image/gif;base64,{data_url}" alt="destilacion" style="width: 300px;">',
            unsafe_allow_html=True,
        )

        # Obtener temperaturas de ebullición únicas y convertirlas a una lista para el selectbox
        temperaturas = df["Ebullicion"].dropna().unique()  # Aseguramos que no haya NaN
        temperaturas = sorted(temperaturas)  # Ordenar las temperaturas

        # Select box para elegir la temperatura de ebullición
        temperatura_seleccionada = st.selectbox("Selecciona la temperatura de ebullición", temperaturas)

        # Mostrar tabla con los datos de Ebullicion, ndl, ndv
        if temperatura_seleccionada:
            datos_destilacion = df[df["Ebullicion"] == temperatura_seleccionada]
            if not datos_destilacion.empty:
                st.write(f"Datos para la temperatura de ebullición {temperatura_seleccionada}°C:")
                st.write(datos_destilacion[["Ebullicion", "ndl", "ndv"]])
            else:
                st.error("No se encontraron datos para la temperatura seleccionada.")



