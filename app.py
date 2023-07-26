import streamlit as st

from utils import OpenMeteoAPIConnection

open_meteo_conn = st.experimental_connection("open_meteo", type=OpenMeteoAPIConnection)

latitude = st.number_input("Latitude:")
longitude = st.number_input("Longitude:")

if st.button("Get Hourly Temperature Forecast"):
    if latitude:
        temp_data = open_meteo_conn.query_hourly_temp_forecast(
            latitude=latitude, longitude=longitude)

        if temp_data is not None:
            st.dataframe(data=temp_data)
            print(temp_data.columns)
        
        else:
            st.error("Failed to fetch weather data")
