import streamlit as st
import requests
import utils.sidebar as sb

st.set_page_config(page_title="Inicio", page_icon="🏠")
with open("data/jobs.csv", "r", encoding="utf-8") as file:
    jobs_list = [line.strip().replace('"', '') for line in file]

sb.show_sidebar()

st.markdown("<h1 style='text-align: center;'>Predicción de Fraude en Transacciones 🔍</h1>",
            unsafe_allow_html=True)
st.title("")
st.write("Basado en la información obtenida del conjunto de datos se necesita realizar un envío de datos:")
st.markdown("<h2 style='text-align: center;'>Datos para predicción</h2>",
            unsafe_allow_html=True)

with st.form("prediction"):
    st.subheader(":orange[Datos de la Transacción]")

    trans_date_trans_time = st.text_input(
        "Fecha y Hora de la Transacción", placeholder="Ej: 2019-11-09 21:13:09")
    cc_num = st.text_input("Número de Tarjeta de Crédito",
                           placeholder="Ej: 30235438713303")
    merchant = st.text_input(
        "Comercio", placeholder="Ej: fraud_Reichert, Rowe and Mraz")
    category = st.selectbox(
        "Categoría", ["entertainment", "food_dining", "gas_transport", "grocery_net", "grocery_pos",
                      "health_fitness", "home", "kids_pets", "misc_net", "misc_pos", "personal_care",
                      "shopping_net", "shopping_pos", "travel"])

    trans_amount = st.number_input(
        "Monto de la Transacción", min_value=0.0, step=0.01, placeholder="5,44")

    st.subheader(":orange[Datos del Cliente]")

    first_name_col, last_name_col = st.columns(2)
    first_name = first_name_col.text_input("Nombre", placeholder="James")
    last_name = last_name_col.text_input("Apellido", placeholder="Baldwin")
    gender = st.selectbox("Género", ["M", "F"], index=0)
    street = st.text_input("Calle", placeholder="3603 Mitchell Court")
    city = st.text_input("Ciudad", placeholder="Winfield")
    state_code = st.selectbox("Código de Estado",
                              ["AK", "AL", "AR", "AZ", "CA", "CO", "CT", "DC", "DE", "FL",
                               "GA", "HI", "IA", "ID", "IL", "IN", "KS", "KY", "LA", "MA",
                               "MD", "ME", "MI", "MN", "MO", "MS", "MT", "NC", "ND", "NE",
                               "NH", "NJ", "NM", "NV", "NY", "OH", "OK", "OR", "PA", "RI",
                               "SC", "SD", "TN", "TX", "UT", "VA", "VT", "WA", "WI", "WV",
                               "WY"], index=18)
    zip_code = st.text_input("Código Postal", placeholder="25213")
    city_population = st.number_input(
        "Población de la Ciudad", min_value=0, placeholder=5512, step=1)
    job = st.selectbox("Ocupación", jobs_list, index=119)
    dob = st.date_input("Fecha de Nacimiento",
                        format="YYYY-MM-DD", value="1980-03-24")

    submitted = st.form_submit_button("🔍 Enviar Predicción")

    if submitted:
        user_data = {
            "trans_date_trans_time": trans_date_trans_time,
            "cc_num": cc_num,
            "merchant": merchant,
            "category": category,
            "trans_amount": trans_amount,
            "first_name": first_name,
            "last_name": last_name,
            "gender": gender,
            "street": street,
            "city": city,
            "state_code": state_code,
            "zip": zip_code,
            "city_population": city_population,
            "job": job,
            "dob": str(dob)
        }

        api_url = st.secrets["api"]["url_api"]

        response = requests.post(api_url, json=user_data)

        if response.status_code == 200:
            api_response = response.json()

            if "prediction" in api_response:
                prediction = api_response["prediction"]
                st.success("✅ Datos enviados correctamente")

                if prediction == 1:
                    st.markdown("""
                        <div>
                            <h3 style="color: red;">🛑 Hay Fraude</h3>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div>
                        <h3 style="color: green;">✅ No Hay Fraude</h3>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.error(
                    "❌ La respuesta de la API no contiene el campo 'prediction'.")
                st.json(api_response)
        else:
            st.error(f"❌ Error al enviar los datos: {response.status_code}")
            st.write(response.text)
