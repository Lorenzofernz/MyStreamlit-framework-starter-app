import streamlit as st
from datetime import date, time
import pandas as pd
import numpy as np
import time as tm
import pydeck as pdk
import plotly.express as px
import requests
import json

st.set_page_config(
    page_title="HCI - Streamlit",

    layout = "wide",
    menu_items={
        'Get Help': 'https://docs.streamlit.io/',
        'Report a bug':  "http://localhost:8501",
        'About': '# Welcome to HCI. Developed by Lorenzo Fernandez'

    }
)

st.title("Learning Streamlit")

st.header("HCI - Lorenzo Fernandez")

add_selectbox = st.sidebar.selectbox(
    "Select the Project",
    ["Homepage", "Geological Periods", "United States Capitals", "Monitoring Biscayne Bay", "Crypto"]
)
if add_selectbox == "Geological Periods":
    # Dividing the screen into 3 columns
    col1, col2, col3 = st.columns(3)
    # Populating each column
    with col1:
        # Creating a dataframe for the geological periods
        geological_periods = pd.DataFrame(
            {
                "Geological Period" : ["Quaternary", "Neogene", "Paleogene", "Cretaceous", "Jurassic", "Triassic"],
                "Millions of Years" : [2.588, 23.03, 66, 145.5, 201.3, 252.17]
            }
        )
        # Displaying the dataframe
        st.dataframe(geological_periods)
        st.caption("Geological periods in millions of years ago")

    with col2:
        st.image("media/sedona_usa.jpeg")
        st.caption("Sedona, Arizona, USA, by Edmundo Mendez Jr, 2020")

    with col3:
        st.video("media/volcano.mp4")
        st.caption("Volcano by Martin Sanchez")


elif add_selectbox == "United States Capitals":
    col1, col2 = st.columns(2)

    with col1:
        # Reading the csv file for the USA capitals
        usa_capitals = pd.read_csv('csv/capitals_usa.csv')
        # Displaying the data as a dataframe
        st.dataframe(usa_capitals)
        st.caption("Table of the 50 states of the USA with their respective city capitals and their coordinates.")

    with col2:
        st.map(usa_capitals)
        st.caption("Map marking the city capitals of all the states in the USA.")



elif add_selectbox == "Monitoring Biscayne Bay":
    st.subheader("1 - Map - Water Quality Parameteres")
    uploaded_file = st.file_uploader("Choose a CSV file (if none is provided, a default dataset will be shown.")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_csv("csv/biscayne_bay_dataset_dec_2021.csv")

    zoom_lat = df["latitude"].mean()
    zoom_long = df["longitude"].mean()

    st.pydeck_chart(
        pdk.Deck(
            # map_style https://docs.mapbox.com/api/maps/styles/
            map_style='mapbox://styles/mapbox/satellite-streets-v11',
            initial_view_state=pdk.ViewState(
                latitude=zoom_lat,
                longitude=zoom_long,
                zoom=18,
                pitch=50,
            ),
            layers=[
                pdk.Layer(
                    'ScatterplotLayer',
                    data=df,
                    get_position='[longitude, latitude]',
                    get_color='[26, 255, 0, 160]',
                    get_radius=0.25,
                    pickable=True,
                ),
            ],
            tooltip={
                "html": "Lat: {latitude} <br/> Long:{longitude} <br/> ODO(mg/L):{ODO (mg/L)} <br/>"
                        "Temp(C): {Temperature (C)} <br/> pH: {pH} <br/> TWC(m): {Total Water Column (m)} <br/>",
                "style": {
                    "backgroundColor": "steelblue",
                    "color": "white"
                }
            }
        )
    )

    with st.expander("See definitions for the water quality parameters"):
        st.write("- Total Water Column (m): measure of depth from the surface to the bottom of the ocean. \n"
                 "Temperature (C): physical property that expresses how hot or cold (average thermal engergy) the water is.\n"
                 "- pH: measure of how acidic or basic the water is, ranging from 0 to 14, with 7 being neurtral. <7 indicates acidity, whereas >7 indicates a base. \n"
                 "- ODO (mg/L): concentration of molecular ocygen (O2) dissolved in water.")

    st.subheader("2 - Plots - Water Quality Parameters")
    col1, col2 = st.columns(2)

    with col1:
        water_parameter = st.radio(
            "Select a water parameter",
            ["ODO (mg/L)", "Temperature (C)", "pH", "Total Water Column (m)"]
        )

    with col2:
        color = st.color_picker("Pick a color", "#00f900")
        st.write("The chosen color is", color)

    if water_parameter:
        fig = px.line(
            df,
            x = df.index,
            y = water_parameter,
            title = water_parameter
        )
        fig.update_traces(line_color=color)
        st.plotly_chart(fig,use_container_width=True)

    st.subheader("3 - 3D Plot for the Total Water Column")
    fig2 = px.scatter_3d(df,
                        x="longitude",
                        y="latitude",
                        z="Total Water Column (m)",
                        color= "Total Water Column (m)"
                        )
    fig2.update_scenes(zaxis_autorange="reversed")
    fig2.update_scenes(xaxis_autorange="reversed")
    fig2.update_scenes(yaxis_autorange="reversed")
    st.plotly_chart(fig2)

    st.subheader("4 - Table - Water Quality Parameters")
    parameters= st.multiselect(
        "Select One or More Parameters",
        ["ODO (mg/L)", "Temperature (C)", "pH", "Total Water Column (m)"]
    )
    st.dataframe(df[["latitude", "longitude"]+ parameters])

    st.subheader("5 - Descriptive Statistics - Water Quality Parameters")
    st.dataframe(df.describe())


elif add_selectbox == "Crypto":
    st.title("Currency Monitoring")
    st.header("Find the latest crypto price updates")

    crypto = st.selectbox("Choose a cryptocurrency",
                          options=["Bitcoin", "Ethereum", "Litecoin"]
                          )
    if crypto == "Bitcoin":
        url = "https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD"
        response = requests.get(url).json()
        #  st.write(response)
        btc_price = response["USD"]
        st.write("The current price of bitcoin is US$ {}".format(btc_price))

    if crypto == "Ethereum":
        url = "https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD"
        response = requests.get(url).json()
        #  st.write(response)
        btc_price = response["USD"]
        st.write("The current price of ethereum is US$ {}".format(btc_price))

    if crypto == "Litecoin":
        url = "https://min-api.cryptocompare.com/data/price?fsym=LTC&tsyms=USD"
        response = requests.get(url).json()
        #  st.write(response)
        btc_price = response["USD"]
        st.write("The current price of litecoin is US$ {}".format(btc_price))


    def currency_conversion(cost, currency):
        file = open("api_keys.json")
        json_file = json.load(file)
        # st.write(type(file),type(json_file))
        api_key = json_file["currency_api"]
        url = "http://api.currencylayer.com/live?access_key=" + api_key
        response = requests.get(url).json()
        st.write(response)
        desiredCurrency = "USD" + currency
        value = response["quotes"][desiredCurrency]
        converted_cost = cost / value
        return converted_cost


    st.header("Currency Converter")

    currency = st.radio("Choose a currency",
                        options=["BRL", "EUR", "BTC"]
                        )
    value = st.number_input("Enter cost to be")

    if value and currency == "BRL":
        st.subheader("Brazilian Real")
        converted_cost = currency_conversion(value, currency)
        st.write("R {:.2f} is equivalent to US$ {:.2f}.".format(value, converted_cost))

    elif value and currency == "EUR":
        st.subheader("Euro")
        converted_cost = currency_conversion(value, currency)
        st.write("€ {:.2f} is equivalent to US$ {:.2f}.".format(value, converted_cost))

    elif value and currency == "BTC":
        st.subheader("Bitcoin")
        converted_cost = currency_conversion(value, currency)
        st.write(" {:.2f} is equivalent to US$ {:.2f}.".format(value, converted_cost))

else:
    st.subheader("Personal Info")

    first_name = st.text_input('First Name')
    last_name = st.text_input('Last Name')
    major = st.selectbox('What is your major',
                         ["Computer Science", "Information Technology", "CyberSecurity", "Data Science"])
    campus = st.radio('Which campus are you at?',
                      ["MMC", "BBC", "EC"])
    date_started = st.date_input("Start Date at FIU")
    today = date.today().year

    if first_name and last_name and major and campus and date_started:
        st.write("Hi,", first_name, "! You have been at FIU,", campus, "for", str(today - date_started), "years studying",
                 major, ".")

    campuses_map = st.checkbox("See all of the FIU campuses on the map")
    if campuses_map:
        st.write("User selected the field")
        map_data = pd.DataFrame(
            np.array([
                [25.759005, -80.373825],
                [25.770459, -80.368130],
                [25.910728, -80.138982],
                [25.992332, -80.339832],
                [25.763418, -80.190564],
                [25.790110, -80.131561],
                [24.950351, -80.452974],
                [38.895549, -77.011910],
                [25.772754, -80.134411],
                [25.781113, -80.132460]
            ]),
        columns=['lat', 'lon'])
        st.map(map_data)

    st.subheader("Steamlit Feautures")

    basic_plots = st.checkbox("Basic Plots")
    if basic_plots:
        chart_data = pd.DataFrame(
            np.random.rand(20,4),
        columns=["A","B","C","D",]
            )
        st.line_chart(chart_data)

    sliders = st.checkbox("Sliders")
    if sliders:
        st.info("Integer slider for age")
        age = st.slider("How old are you?", 0,100,21)
        st.write("I'm", str(age), "years old.")

        st.info("Time slider for appointment")
        appointment = st.slider(
            "Schedule an appointment:",
            value= (time(11,30), time(12,45))
        )
        st.write("You are scheduled for:",
                 appointment[0].strftime("%H:%M"),
                 "to", appointment[1].strftime("%H:%M"))

        st.info("Float slider for a range")
        values = st.slider("Select a range of values",
                           0.0,100.0, (25.0,75.0))
        st.write("Values:", str(values))

    audio = st.checkbox("Audio")
    if audio:
            st.write("Waves and Birds")
            st.audio("https://bigsoundbank.com/UPLOAD/mp3/0267.mp3", format="media/mp3", start_time=0)

            st.write("Alla Turca by Wolfgang Amadeus Mozart Sonata No. 11")
            st.audio("media/Alla-Turca.mp3", format="media.m3", start_time=0)
            st.caption("License & Usage: Creatove Commons CC BY 3.0")

    boxes = st.checkbox("Check the types of message boxes")
    if boxes:
            st.success("This is a success box.")
            st.warning("This is a warning box.")
            st.error("This is an error box.")
            st.info("This is an info box.")

    balloons = st.checkbox("Surprise!")
    if balloons:
            st.balloons()

    progress_bar = st.checkbox("Progress Bar")
    if progress_bar:
        latest_iteration = st.empty()
        bar = st.progress(0)
        for i in range(100):
            latest_iteration.text(f'Iteration {i+1}')
            bar.progress(i+1)
            tm.sleep(0.1)
