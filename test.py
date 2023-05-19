import streamlit as st
import paho.mqtt.publish as publish

# Thiết lập thông tin MQTT Broker
BROKER = 'broker.hivemq.com'
PORT = 1883
TOPIC = 'door1'

# LED UI
st.title('LED Control')
led_state = st.radio('LED State', ['ON', 'OFF'])
submit_button = st.button('Submit')

# Xử lý sự kiện khi nhấn nút Submit
if submit_button:
    publish.single(TOPIC, led_state, hostname=BROKER, port=PORT)
    st.success('LED state updated successfully!')

placeholder = st.empty()
placeholder.line_chart({"data": [1, 5, 2, 6]})
