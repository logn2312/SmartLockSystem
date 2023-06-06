import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import base64
import requests
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu
from PIL import Image
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import csv
import os
import pandas as pd
import cv2
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
from mtcnn import MTCNN
import time
import facenet

# set MQTT Broker
BROKER = 'broker.hivemq.com'
PORT = 1883
TOPIC1 = 'door1'
TOPIC2 = 'door2'

def on_connect(client, userdata, flags, rc):
    print("Connected")

st.set_page_config(page_title="Homepage",layout="wide")

# Add a sidebar
st.sidebar.title('Navigation')
# Create links in the sidebar

def set_bg_hack(main_bg):
    '''
    A function to unpack an image from root folder and set as bg.
 
    Returns
    -------
    The background.
    '''
    # set bg name
    main_bg_ext = "jpg"
        
    st.markdown(
         f"""
         <style>
         .stApp {{
             background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

#set_bg_hack('background.png')

button_tyle = st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-image: linear-gradient(to right, #E0EAFC 0%, #CFDEF3  51%, #E0EAFC  100%);
        height: 3em;
        width: 7.5em;
        margin: 0 auto;
        padding: 20px;
        text-align: center;
        transition: 0.5s;
        background-size: 200% auto;
        color: #10266F;
        box-shadow: 0 0 20px #eee;
        backdrop-filter: blur( 0px );
        -webkit-backdrop-filter: blur( 0px );
        border-radius: 10px;
        border: 1px solid rgba( 255, 255, 255, 0.18 );
        display: flex;
    }

    div.stButton > button:hover {
        background-position: right center; /* change the direction of the change here */
        color: #fff;
    }

    div.stButton > button:active {
        position:relative;
        top:3px;
    }

    </style>
""", unsafe_allow_html=True)

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
load_coding = load_lottieurl("https://assets7.lottiefiles.com/packages/lf20_6e0qqtpa.json")

image1 = Image.open('logo.png')
image2 = Image.open('robot.png')

with st.container():
    col1, col2 = st.columns([1,1.5])
    with col2:
        with st.container():
            col5, col6, col7, col8, col9 = st.columns(5)
            with col5:
                st.text("")
                st.text("")
                home = st.button('**Homepage**')
                st.write("")
            with col6:
                st.text("")
                st.text("")
                admin = st.button('**Admin**')
                st.image(image2, width = 400)
            with col7:
                st.text("")
                st.text("")
                user = st.button('**User**')
            with col8:
                st.text("")
                st.text("")
                about_us = st.button('**About Us**')
            with col9:
                st.text("")
                st.text("")
                contact = st.button('**Contact Us**')
        with st.container():
            df1 = pd.read_csv("Attendance.csv")
            df2 = pd.read_csv("Schedule.csv")

            Id_list = df1['Id'].tolist()
            Id = Id_list[0]
            for (index, row) in df2.iterrows():
                if (row['Id'] != Id): #Id input từ bàn phím
                    df2 = df2.drop(index)

            room = df2['Room'].tolist()
            with st.container():
                st.write('**Room Status**')
                placeholder1 = st.empty()
                placeholder1.warning("")

            def on_message(client, userdata, message):
                msg = message.payload.decode()
                if msg == 'Unlock':
                    placeholder1.success('Unlock!', icon="✅")
                    time.sleep(5)
                elif msg == 'Lock':
                    placeholder1.error('Lock!', icon="🚨")
                    time.sleep(1)

    with col1:
        col3, col4, _ = st.columns([1,3,1])
        with col3:
            st.image(image1, width = 100)
        st.title("Smart Lock System")
        st_lottie(load_coding, width = 350, height = 200,key="coding")
        st.header("Welcome to my app :heart:")
        if about_us:
            st.header('About Us')
            st.info('This Smart Lock System Based System is designed by International University!')
        elif contact:
            st.header('Contact Us')
            st.info('If you find you need any help contact me on pdtdh@hcmiu.edu.vn!')

        with col4:
            st.text("")
            st.write("VIETNAM NATIONAL UNIVERSITY HCMC")
            st.write("**INTERNATIONAL UNIVERSITY**")
            # Add the main content
            if home:
                switch_page("Homepage")
            elif admin:
                switch_page("Admin")
            elif user:
                switch_page("User")

client = mqtt.Client()
client.connect(BROKER, PORT)
client.subscribe(TOPIC1)
client.subscribe(TOPIC2)
client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()
