import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import base64

# Set page config
st.set_page_config(page_title="Simulador Destilación Etanol-Agua", layout="centered")

# Diccionario con los valores de ndl y ndv para cada temperatura
datos_nd = {
    78: {"ndl": 1.3614, "ndv": 1.3614},
    79: {"ndl": 1.3642, "ndv": 1.3630},
    80: {"ndl": 1.3650, "ndv": 1.3630},
    81: {"ndl": 1.3655, "ndv": 1.3636},
    82: {"ndl": 1.3658, "ndv": 1.3646},
    83: {"ndl": 1.3655, "ndv": 1.3653},
    84: {"ndl": 1.3650, "ndv": 1.3656},
    85: {"ndl": 1.3641, "ndv": 1.3658},
    86: {"ndl": 1.3626, "ndv": 1.3655},
    87: {"ndl": 1.3610, "ndv": 1.3647},
    88: {"ndl": 1.3590, "ndv": 1.3638},
    89: {"ndl": 1.3557, "ndv": 1.3626},
    90: {"ndl": 1.3524, "ndv": 1.3610},
    91: {"ndl": 1.3484, "ndv": 1.3590},
    92: {"ndl": 1.3469, "ndv": 1.3566},
    93: {"ndl": 1.3425, "ndv": 1.3535},
    94: {"ndl": 1.3395, "ndv": 1.3484},
    95: {"ndl": 1.3354, "ndv": 1.3455},
    100: {"ndl": 1.3330, "ndv": 1.3330},
}

# Cargar base de datos desde CSV
@st.cache_data
def cargar_datos():
    df = pd.read_csv("BINARIA.csv")
    df.columns = df.columns.str.strip()  # Eliminar espacios extras de las columnas
    return df

df = cargar_datos()

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
        temperaturas = sorted(datos_nd.keys())  # Usamos las claves del diccionario
        temperatura_seleccionada = st.selectbox("Selecciona la temperatura de ebullición", temperaturas)

        # Si la temperatura es seleccionada, mostramos los valores de ndl y ndv
        if temperatura_seleccionada:
            st.write(f"Datos para la temperatura de ebullición {temperatura_seleccionada}°C:")
            ndl = datos_nd[temperatura_seleccionada]["ndl"]
            ndv = datos_nd[temperatura_seleccionada]["ndv"]
            st.write(f"**ndl**: {ndl}")
            st.write(f"**ndv**: {ndv}")


