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
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import time
import datetime

import yagmail
import smtplib
import imaplib

#setup broker mqtt
BROKER = 'broker.hivemq.com'
PORT = 1883
TOPIC1 = 'door1'
TOPIC2 = 'door2'

#Login to the mail account through IMAP and SMTP

imap = imaplib.IMAP4_SSL('imap.gmail.com',993)                                          
unm = 'longdht.2312@gmail.com'                                                      
psw = 'dtrihdiqdebjzaqo'                                                                 
imap.login(unm,psw) 

mail=smtplib.SMTP('smtp.gmail.com',587)
mail.ehlo()
mail.starttls()
mail.login(unm,psw)

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

def upload_file_to_google_sheet(file_path, spreadsheet_id, sheet_name):
    # Read credentials file JSON
    credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", ["https://www.googleapis.com/auth/spreadsheets"])

    # Create connection to Google Sheets API
    client = gspread.authorize(credentials)

    # Open spreadsheet
    spreadsheet = client.open_by_key(spreadsheet_id)

    # Get sheet by sheet name
    sheet = spreadsheet.worksheet(sheet_name)
    
    sheet.clear()
    
    # Read data from file and write it
    with open(file_path, "r") as file:
        data = pd.read_csv(file)

    # Create list from file
    values = data.values.tolist()
    
    # Write data to sheet
    sheet.insert_rows(values)

def automail():
    recipient = "ITITIU19026@student.hcmiu.edu.vn"
    date = datetime.date.today().strftime("%B %d, %Y")
    sub = "Attendance Report for " + str(date)
    yag = yagmail.SMTP(unm, psw)
    # Read credentials file JSON
    credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", ["https://www.googleapis.com/auth/spreadsheets"])

    # Create connection to Google Sheets API
    client = gspread.authorize(credentials)

    # Open spreadsheet
    spreadsheet = client.open_by_key('1OKvDa6AZxG7RcJzblfAAFlyNZxNqAyyZyRgXRKlAJE8')

    # Get sheet by sheet name
    sheet = spreadsheet.worksheet('Sheet1')
    
    df2 = pd.DataFrame(data=sheet.get_all_records())
    df2.to_csv("Attendance.csv", index=False)
    
    yag.send(
        to=recipient, #recipient email ID
        subject=sub, # email subject
        contents='''Dear Lecturer,

        Here is the Attendance details of your class. Please have a look at the file attached to get more information. If you have any questions or concerns, don't hesitate to contact me during my leave via email or phone.
                
        Thank you & Best Regards,

        Office of Undergraduate Academic Affairs.
        ''',  # email body
        attachments= "Attendance.csv"  # file attached
    )

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
            #room1, room2 = st.columns(2)
            #with room1:
                #with st.container():
            st.write('**Room Status**')
            placeholder1 = st.empty()
            remote_control1 = st.selectbox("**Remote Control Room Door Lock**", ('','Unlock✅','Lock🚨'))
            if remote_control1 == 'Unlock✅':
                led_state = 'ON'
                publish.single(TOPIC1, "Unlock", hostname=BROKER, port=PORT)
                placeholder1.success('Unlock!', icon="✅")
            elif remote_control1 == 'Lock🚨':
                led_state = 'OFF'
                publish.single(TOPIC1, "Lock", hostname=BROKER, port=PORT)
                placeholder1.error('Lock!', icon="🚨")

            def on_message(client, userdata, message):
                msg = message.payload.decode()
                if msg == 'Unlock':
                    placeholder1.success('Unlock!', icon="✅")
                    time.sleep(5)
                elif msg == 'Lock':
                    placeholder1.error('Lock!', icon="🚨")
                    time.sleep(1)
                #publish.single(TOPIC1, led_state, hostname=BROKER, port=PORT)
        placeholder3 = st.empty()
        placeholder4 = st.empty()
        
        selected = option_menu(
            menu_title=None,  # required
            options=["Upload", "Email", "History"],#, "Statistics"],  # required
            icons=["upload", "envelope", "clock-history"],# "activity"],  # optional
            menu_icon="cast",  # optional
            default_index=0,  # optional
            orientation="horizontal",
            styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "icon": {"color": "red"},
                "nav-link": {
                    "text-align": "center",
                    "margin": "0px",
                    "--hover-color": "#eee",
                },
                "nav-link-selected": {"background-color": "#D5C9FE", "color": "#10266f"},
            }
        )
        
        if selected == 'Email':
            automail()
            placeholder3.success('Email Successfully Sent✅')
        elif selected == 'History':
            df = pd.read_csv("Attendance.csv")
            placeholder3.dataframe(df)
        # elif selected == 'Statistics':
        #     placeholder3.line_chart({"data": [1, 5, 2, 6]})
        # Upload file to Google Sheets
        elif selected == 'Upload':
            uploaded_file = placeholder3.file_uploader("Chọn file để tải lên")

            if uploaded_file is not None:
                # Read CSV file into a Pandas DataFrame
                df = pd.read_csv(uploaded_file)
                df.to_csv('file.csv', index= False)
                spread_sheet_id = '10hRdVBjcUzJ5l-U6Ww27gFqGSh4BCyNirHJCKq8ufK0'
                sheet_name = 'Sheet1'  # Tên sheet trong Google Sheets
                upload_file_to_google_sheet('file.csv', spread_sheet_id, sheet_name)
                placeholder4.success('Upload file successfully!')

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
