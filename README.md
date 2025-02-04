# Frontend

## Instrucciones:

- Crear ambiente virtual: `python -m venv nombre_ambiente`
- Instalar requirements: `pip install -r requirements.txt`
> [!IMPORTANT]
> Se debe modificar las conexiones a la base de datos y api, en este caso se uso de los `streamlit secrets` que basicamente en el directorio `.streamlit/` se debe añadir un archivo `secrets.toml` y agregar la información de la siguiente forma:

```TOML
[database]
user="tu_usuario_db"
password="tu_clave_db"
host="tu_server_db"
port="tu_puerto_db"
dbname="tu_base_datos"
[api]
url_api="tu_server_api"
```

- Ejecutar streamlit: `streamlit run 0_🏡_home.py`
