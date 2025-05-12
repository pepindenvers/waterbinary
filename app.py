import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import base64

# Encabezado
st.title("🧪 Simulador de Destilación Etanol-Agua")
st.markdown("""
Este simulador permite medir el índice de refracción de una mezcla etanol-agua y realizar una simulación de destilación para observar el comportamiento de la mezcla en función de su composición.
""")

# Datos de ndl y ndv por temperatura (ya no se usa CSV para esto)
datos_nd = pd.DataFrame({
    "Ebullicion": [78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,100],
    "ndl": [1.3614,1.3642,1.365,1.3655,1.3658,1.3655,1.365,1.3641,1.3626,1.361,1.359,1.3557,1.3524,1.3484,1.3469,1.3425,1.3395,1.3354,1.333],
    "ndv": [1.3614,1.363,1.363,1.3636,1.3646,1.3653,1.3656,1.3658,1.3655,1.3647,1.3638,1.3626,1.361,1.359,1.3566,1.3535,1.3484,1.3455,1.333]
})

# Cargar base de datos desde CSV (BINARIA.csv)
@st.cache_data
def cargar_datos():
    df = pd.read_csv("BINARIA.csv")
    df.columns = df.columns.str.strip()  # Limpiar nombres de columnas
    return df

df = cargar_datos()

# Paso 1: Selección de porcentaje
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

        # Sección de destilación
        st.markdown("### 🔥 Destilar")
        
        # Mostrar gif
        file_ = open("destila.gif", "rb")
        contents = file_.read()
        data_url = base64.b64encode(contents).decode("utf-8")
        file_.close()
        st.markdown(
            f'<img src="data:image/gif;base64,{data_url}" alt="destilacion" style="width: 300px;">',
            unsafe_allow_html=True,
        )

        # Mostrar tabla completa de ebullición, ndl y ndv
        st.markdown("#### Tabla de Temperaturas de Ebullición con ndl y ndv")
        st.dataframe(datos_nd, use_container_width=True)



