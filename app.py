import streamlit as st
import pandas as pd

from utils import OpenMeteoAPIConnection, create_hourly_df

open_meteo_conn = st.experimental_connection("open_meteo", type=OpenMeteoAPIConnection)

st.markdown(
    """
## Simple Weather Forecast  
  

Built using the [Open-Meteo](https://open-meteo.com/) weather models and [Streamlit](https://streamlit.io/).  
Enter the coordinates below.  
            """
)

latitude = st.number_input("Latitude:", value=1.35, min_value=-90.0, max_value=90.0)
longitude = st.number_input(
    "Longitude:", value=103.8, min_value=-180.0, max_value=179.9
)

if st.button("Get Hourly Forecast"):
    temp_data = open_meteo_conn.query_hourly_forecast(
        latitude=latitude, longitude=longitude
    )

    temperature_df, precipitation_df, wind_df, uv_df = create_hourly_df(temp_data)

    st.text("")
    st.header("Temperature Forecast(°C)")
    st.line_chart(temperature_df)
    st.text("")
    st.header("Precipitation Probability(%)")
    st.line_chart(precipitation_df)
    st.text("")
    st.header("Wind Speed at 10m (km/h)")
    st.line_chart(wind_df)
    st.text("")
    st.header("UV Index")
    st.line_chart(uv_df)
