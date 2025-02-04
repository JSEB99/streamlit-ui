import utils.sidebar as sb
import streamlit as st
import pandas as pd
import utils.charts as ch
import utils.queries as q

CARD_BG_COLOR = "#00a400"
CARD_TITLE_COLOR = "#043616"
CARD_VALUE_COLOR = "white"
CHART_COLOR = "#00a400"

st.set_page_config(page_title="Inicio", page_icon="🏠")

sb.show_sidebar()

st.markdown("<h1 style='text-align: center;'>Bienvenido a la App de Detección de Fraude 🏠</h1>",
            unsafe_allow_html=True)
st.write("Esta aplicación ayuda a identificar transacciones fraudulentas.")
st.markdown('<h2 style="background-color: #00a400; color: white; padding: 5px; border-radius: 5px; text-align: center;">Análisis Descriptivo</h2>',
            unsafe_allow_html=True)

with st.container():
    st.markdown("### Transacciones")
    engine = ch.connection()
    five_rows = ch.get_cached_data(q.FIVE_ROWS)
    st.dataframe(data=five_rows)

    total_trans, total_fraud, max_trans, min_trans = st.columns(4)

    describe_cards = ch.get_cached_data(q.CARDS_DESC_STATS)
    with total_trans:
        ch.cards(CARD_BG_COLOR, CARD_TITLE_COLOR,
                 "Transacciones Totales", CARD_VALUE_COLOR, describe_cards["total"].values[0])
    with total_fraud:
        ch.cards(CARD_BG_COLOR, CARD_TITLE_COLOR,
                 "Transacciones Fraudulentas", CARD_VALUE_COLOR, describe_cards["total_fraud"].values[0])
    with max_trans:
        ch.cards(CARD_BG_COLOR, CARD_TITLE_COLOR,
                 "Monto Máximo", CARD_VALUE_COLOR, describe_cards["max_amount"].values[0])
    with min_trans:
        ch.cards(CARD_BG_COLOR, CARD_TITLE_COLOR,
                 "Monto Mínimo", CARD_VALUE_COLOR, describe_cards["min_amount"].values[0])

    st.markdown("<br></br>", unsafe_allow_html=True)

    trans_month = ch.get_cached_data(q.TRANS_MONTH)
    trans_weekday = ch.get_cached_data(q.TRANS_WEEKDAY)
    per_month, per_weekday = st.columns(2)

    with per_month:
        st.write("Transacciones totales por Mes")
        st.bar_chart(trans_month, x="mes",
                     y="total transacciones", stack=False, color=CHART_COLOR)
    with per_weekday:
        st.write("Transacciones totales por día de la semana")
        st.bar_chart(trans_weekday, x="dia de la semana",
                     y="total transacciones", stack=False, color=CHART_COLOR)

st.markdown("""<h2 style='background-color: #00a400; color: white; padding: 5px;
            border-radius: 5px; text-align: center;'>Análisis Exploratorio <span style='color:#043616;'>(Enfocado al Fraude)</span></h2>""",
            unsafe_allow_html=True)
with st.container():
    st.markdown("<h3 style='color:orange;text-align:center;'>Frecuencia de Fraudes</h3>",
                unsafe_allow_html=True)
    fraudes_per_1k, fraudes_per_weekday = st.columns(2)
    trans_fraud_1k_month = ch.get_cached_data(q.FRAUD_1K_MONTH)
    trans_fraud_1k_weekday = ch.get_cached_data(q.FRAUD_1K_WEEKDAY)
    trans_fraud_1k_time = ch.get_cached_data(q.FRAUD_1K_TIME)
    with fraudes_per_1k:
        st.write("Fraudes por cada 1000 transacciones")
        st.bar_chart(trans_fraud_1k_month, x="mes",
                     y="fraudes c/1000", stack=False, color=CHART_COLOR)
    with fraudes_per_weekday:
        st.write("Fraudes por día de la semana por cada 1000 transacciones")
        st.bar_chart(trans_fraud_1k_weekday, x="dia de la semana",
                     y="fraudes c/1000", stack=False, color=CHART_COLOR)
    st.write("¿Hay franjas horarias con más fraudes?")
    st.write("Hora con mas fraudes por cada 1000 transacciones")
    st.line_chart(trans_fraud_1k_time, x="hora",
                  y="fraudes c/1000", color=CHART_COLOR)

trans_fraud_1k_category = ch.get_cached_data(q.FRAUD_1K_CATEGORY)
trans_fraud_1k_state = ch.get_cached_data(q.FRAUD_1K_STATE)

with st.container():
    st.markdown("<h3 style='color:orange;text-align:center;'>Categoría del Negocio</h3>",
                unsafe_allow_html=True)
    st.write("Transacciones con Fraude por Categoría cada 1000 transacciones")
    st.bar_chart(trans_fraud_1k_category, x="categorias",
                 y="fraudes c/1000", stack=False, color=CHART_COLOR)
    st.markdown("<h3 style='color:orange;text-align:center;'>Ubicación Geográfica</h3>",
                unsafe_allow_html=True)
    st.write("¿Existen estados con mayor concentración de fraudes?")
    st.write("Estados con transacciones fraudulentas por cada 1000 habitantes")
    st.bar_chart(trans_fraud_1k_state, x="código estado",
                 y="fraudes c/1000", stack=False, color=CHART_COLOR)
    correlation, city_max, city_max_frauds = st.columns(3)

    correlation_df = ch.get_cached_data(q.CORR_POB_FRAUD)
    city_max_df = ch.get_cached_data(q.CITY_MAX_FRAUD)
    city_max_trans_df = ch.get_cached_data(q.CITY_MAX_TRANS)

    with correlation:
        ch.cards(CARD_BG_COLOR, CARD_TITLE_COLOR,
                 "Correlación Población x Cant. Fraudes", CARD_VALUE_COLOR,
                 correlation_df["corr población fraude"].values[0])
    with city_max:
        ch.cards(CARD_BG_COLOR, CARD_TITLE_COLOR,
                 "Ciudad con mas Fraudes", CARD_VALUE_COLOR,
                 str(city_max_df["ciudad"].values[0])+": " +
                 str(city_max_df["transacciones fraudulentas"].values[0]),
                 "20px")
    with city_max_frauds:
        ch.cards(CARD_BG_COLOR, CARD_TITLE_COLOR,
                 "Ciudad con mas Transacciones", CARD_VALUE_COLOR,
                 str(city_max_trans_df["ciudad"].values[0])+": " +
                 str(city_max_trans_df["transacciones totales"].values[0]),
                 "20px")

with st.container():
    st.markdown("<h3 style='color:orange;text-align:center;'>Perfíl del Cliente</h3>",
                unsafe_allow_html=True)

    genero_df = ch.get_cached_data(q.FRAUD_GENDER)
    edad_df = ch.get_cached_data(q.FRAUD_AGE)
    trabajos_df = ch.get_cached_data(q.FRAUD_JOB)

    genero, edad = st.columns(2)
    with genero:
        st.write("Transacciones con Fraude por Genero")
        st.bar_chart(genero_df, x="género", y="fraudes",
                     stack=False, color=CHART_COLOR)
    with edad:
        st.write("Transacciones con Fraude por Edad")
        st.bar_chart(edad_df, x="edad", y="fraudes",
                     stack=False, color=CHART_COLOR)
    st.write("Top 5 Transacciones con Fraude por Trabajo")
    st.bar_chart(trabajos_df, x="trabajos", y="fraudes",
                 stack=False, color=CHART_COLOR)
