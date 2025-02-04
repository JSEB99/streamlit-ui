import streamlit as st
import utils.sidebar as sb

st.set_page_config(
    page_title="Aplicación de Detección de Fraude",
    layout="wide",
    page_icon="👾")

sb.show_sidebar()

st.header("Bienvenido a la Aplicación de Detección de Fraude", divider="green")

st.image("./assets/images/ccard.png")
st.subheader("Descripción")
st.text("Se trata de un desarrollo para una plataforma de e-commerce que requiere analizar las transacciones producidas en un período de tiempo, con el objetivo de predecir fraudes a futuro. Para ello, como la empresa tiene diferentes vendedores que ofrecen sus productos, nos envío un dataset de datos de compras realizadas a sus diferentes merchants que fueron realizadas desde la plataforma y resultaron ser fraudes.")
st.subheader("Objetivo")
st.text("Detección y prevención de fraudes con tarjetas de crédito.")
