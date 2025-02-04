import streamlit as st
import utils.sidebar as sb

sb.show_sidebar()

st.header("📩 Contacto", divider="green")

st.subheader("Integrantes:")
name, github = st.columns(2)

name.write("Jairo Ordóñez")
github.markdown('[GitHub](https://github.com/jairodpac)')

name.write("Sebastian Mora")
github.markdown('[GitHub](https://github.com/JSEB99)')

name.write("Georgina Máscolo")
github.markdown('[GitHub](https://github.com/GeoArg)')

st.subheader(":orange[No Country]")
st.markdown(
    "Proyecto de [simulación laboral cohorte 23](https://www.nocountry.tech/)")
