import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform

# Configuración inicial de la página
st.set_page_config(page_title="Control MQTT", page_icon="🔌", layout="centered")

# Encabezado principal
st.title("🔌 Panel de Control MQTT")
st.caption("Control y monitoreo de dispositivos usando protocolo MQTT")

# Información del sistema
with st.expander("🖥️ Información del sistema"):
    st.write("Versión de Python:", platform.python_version())

# Variables globales
values = 0.0
act1 = "OFF"

# Función cuando se publica un mensaje
def on_publish(client, userdata, result):
    print("El dato ha sido publicado\n")
    pass

# Función cuando se recibe un mensaje
def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received = str(message.payload.decode("utf-8"))
    st.success(f"Mensaje recibido: {message_received}")

# Configuración del cliente MQTT
broker = "157.230.214.127"
port = 1883
client1 = paho.Client("GIT-HUB")
client1.on_message = on_message

# Sección de control digital
st.subheader("⚙️ Control de Encendido/Apagado")

col1, col2 = st.columns(2)

with col1:
    if st.button('🟢 Encender (ON)'):
        act1 = "ON"
        client1 = paho.Client("GIT-HUB")
        client1.on_publish = on_publish
        client1.connect(broker, port)
        message = json.dumps({"Act1": act1})
        client1.publish("cmqtt_s", message)
        st.success("Dispositivo encendido.")

with col2:
    if st.button('🔴 Apagar (OFF)'):
        act1 = "OFF"
        client1 = paho.Client("GIT-HUB")
        client1.on_publish = on_publish
        client1.connect(broker, port)
        message = json.dumps({"Act1": act1})
        client1.publish("cmqtt_s", message)
        st.success("Dispositivo apagado.")

# Sección de control analógico
st.subheader("🎚️ Control de Valor Analógico")

values = st.slider('Selecciona el valor analógico a enviar', 0.0, 100.0, step=1.0)
st.write(f'Valor seleccionado: **{values}**')

if st.button('📤 Enviar valor analógico'):
    client1 = paho.Client("GIT-HUB")
    client1.on_publish = on_publish
    client1.connect(broker, port)
    message = json.dumps({"Analog": float(values)})
    client1.publish("cmqtt_a", message)
    st.success(f"Valor {values} enviado correctamente.")

# Footer opcional
st.markdown("---")
st.caption("Desarrollado por Cami 💻")


