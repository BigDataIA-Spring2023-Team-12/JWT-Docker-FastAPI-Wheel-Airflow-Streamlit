import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from streamlit_option_menu import option_menu

# df = pd.read_json(admin_data,lines=True)
#         print(df)

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)
# --- CONNECT TO PASSWORD DATABAE ---
# --- USER AUTHENTICATION ---
# --- REGISTER USER ---
# if authentication_status != True: 
#     landing_menu = option_menu(
#             menu_title=None,
#             options=["Login", "Change Password"],
#             # icons=["house-door", "rocket", "airplane", "geo-fill"],
#             default_index=0,
#             orientation="horizontal"
#         )

authentication_status = None
st.write('## Log In')
login_username = st.text_input('Username')
login_password = st.text_input('Password', type='password')
if st.button('Log In!'):
    authentication_status = True
    pass               #<------- Enpoint Connection

st.write('## Change Password')
fp_username = st.text_input('Username',key='Fp_username')
fp_old_password = st.text_input('Current Password')
fp_new_password = st.text_input('New Password')
if st.button('Change Password'):
    pass                #<------- Enpoint Connection



if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")

if authentication_status:
    # --- OPTION MENU ----
    selected = option_menu(
        menu_title=None,
        options=["Home", "GEOS", "NexRad", "Locations"],
        icons=["house-door", "rocket", "airplane", "geo-fill"],
        default_index=0,
        orientation="horizontal"
    )
    if selected == "Home":
        st.write("# Welcome! 👋")
        st.markdown(
            """
            # Assignment 1
            ## Team 14
            - Parva Shah 
            - Dev Shah
            - Harsh Shah

            This streamlit app has 3 pages:
            - 1_🛰_Geos_Data_Downloader:

                There are ywo methods to download a file:
                - Download by Path:
                User select the path and all files located on that path is displayed. The user can then select a file to download
                - Download by Filename:
                User writes the filename in the input box and a download link for the same is displayed.

            - 2_📡_Nexrad_Data_Downloader
            
                There are ywo methods to download a file:
                - Download by Path:
                User select the path and all files located on that path is displayed. The user can then select a file to download
                - Download by Filename:
                User writes the filename in the input box and a download link for the same is displayed.

            - 3_📍_NexRad_Locations
                This plots the Nexrad locations on the US map

        """
        )

    if selected == "GEOS":
        st.write("# GEOS Satellite Data Downloader 🛰")
        search_method = st.selectbox(
            "Select Search Method",
            ["Search by Filename", "Search by Path"]
        )

        if search_method == "Search by Path":
            pass
        if search_method == "Search by Filename":
            pass

    if selected == "NexRad":

        st.write("# NexRad Data Downloader 📡")
        search_method = st.selectbox(
            "Select Search Method",
            ["Search by Filename", "Search by Path"]
        )

        if search_method == "Search by Path":
            pass
        if search_method == "Search by Filename":
            pass

    if selected == "Locations":
        st.write("# Nexrad Locations in USA 📍")
        # filename issue
        df = pd.read_csv('./nexrad_loc.csv')
        df['text'] = 'City: ' + df['City'] + ', ' + 'State: ' + df["State"] + ', ' + 'Identifier: ' + df[
            'ICAO Location Identifier'].astype(str)

        fig = go.Figure(data=go.Scattergeo(
            lon=df['Long'],
            lat=df['Lat'],
            text=df['text'],
            mode='markers',
        ))

        fig.update_layout(
            title='NexRad Locations',
            geo_scope='usa',
            geo=dict(bgcolor='rgba(0,0,0,0)',
                     lakecolor='#4E5D6C',
                     landcolor='rgba(51,17,0,0.2)',
                     subunitcolor='grey'),

        )
        st.plotly_chart(fig, use_container_width=True)

    # ---- SIDEBAR ----


st.sidebar.write('## Sign up')
name = st.sidebar.text_input('Name')
username = st.sidebar.text_input('Username',key='signup_username')
plan = st.sidebar.selectbox(
            "Select Plan",
          ["free", "gold","platinum"]
        )

password = st.sidebar.text_input('Password', type='password',key='signup_pass')
confirm_password = st.sidebar.text_input('Confirm Password', type='password')

if password == confirm_password:
    st.sidebar.write("Password Match!")
    if st.sidebar.button('Sign up'):
        if password != confirm_password or len(password) <= 0:
            st.sidebar.write("Passwords don't match, Try Again!")
        pass

