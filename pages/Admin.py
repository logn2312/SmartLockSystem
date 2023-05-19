import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import base64
import requests
from streamlit_lottie import st_lottie
from PIL import Image
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt

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
    col1, col2 = st.columns(2)
    with col2:
        with st.container():
            col5, col6, col7, col8, col9, col10 = st.columns(6)
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
                st.text("")
                st.text("")
                st.image(image2, use_column_width = 'always')
            with col10:
                st.text("")
                st.text("")
                contact = st.button('**Login**')
    with col1:
        col3, col4, _ = st.columns([1,3,1])
        with col3:
            st.image(image1, width = 110)
        with col4:
            st.text("")
            st.write("VIETNAM NATIONAL UNIVERSITY HCMC")
            st.write("**INTERNATIONAL UNIVERSITY**")
            st.title("Smart Lock System")
            st_lottie(load_coding, width = 300, height = 200,key="coding")
            # Add the main content
            if home:
                switch_page("Homepage")
            elif admin:
                switch_page("Admin")
            elif user:
                switch_page("User")
            elif about_us:
                st.header('About Us')
                st.info('This Smart Lock System Based System is designed by International University!')
            elif contact:
                st.header('Contact Us')
                st.info('If you find you need any help contact me on pdtdh@hcmiu.edu.vn!')

with st.container():
    login_col, func_col = st.columns(2)
    with login_col:
        _, _ , login_col2, _, _= st.columns(5)
        with login_col2:
            st.button('Login')
    with func_col:
        col1, col2 = st.columns(2)
        with col1:
            if st.button('Room 1'):
                st.success("**Unlock**")
                placeholder = st.empty()
                placeholder.line_chart({"data": [1, 5, 2, 6]})
            else:
                st.error("**Lock**")
        with col2:
            if st.button('Room 2'):
                st.success("**Unlock**")
            else:
                st.error("**Lock**")