import streamlit as st
import pandas as pd
import altair as alt

from utils import OpenMeteoAPIConnection

open_meteo_conn = st.experimental_connection("open_meteo", type=OpenMeteoAPIConnection)

latitude = st.number_input("Latitude:", value=1.35, min_value=-90.0, max_value=90.0)
longitude = st.number_input(
    "Longitude:", value=103.8, min_value=-180.0, max_value=179.9
)

if st.button("Get Hourly Temperature Forecast"):
    temp_data = open_meteo_conn.query_hourly_temp_forecast(
        latitude=latitude, longitude=longitude
    )

    # if temp_data is not None:
    #     # st.write(temp_data)

    # else:
    #     st.error("Failed to fetch weather data")
    df = pd.DataFrame(
        data={
            "Temperature": temp_data["hourly"]["temperature_2m"],
            "Apparent Temperature": temp_data["hourly"]["apparent_temperature"],
        },
        index=temp_data["hourly"]["time"],
    )

    st.line_chart(df)

    with st.expander("Show dataframe"):
        st.dataframe(df)
