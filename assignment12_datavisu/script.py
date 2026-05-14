import streamlit as st
import pandas as pd
from streamlit_gps_location import gps_location_button

# Page configuration
st.set_page_config(
    page_title="My Mobile App",
    layout="centered"
)

st.title("Streamlit mobile app")

# User input
name = st.text_input("What is your name?")
age = st.slider("How old are you?", 0, 100, 25)

# GPS location
st.subheader("Location")
location_data = gps_location_button(buttonText="Get my location")

# Only create the map if we have valid location data
if location_data is not None:
    st.write("Your location data:")
    st.json(location_data)

    # Ensure latitude and longitude are not None
    if location_data.get('latitude') is not None and location_data.get('longitude') is not None:
        map_data = pd.DataFrame({
            'lat': [location_data['latitude']],
            'lon': [location_data['longitude']]
        })
        st.subheader("Your location on the map")
        st.map(map_data)
else:
    st.info("Press 'Get my location' to see your location on the map.")

# Submit button
if st.button("Submit", use_container_width=True):
    st.success(f"Hello {name}, you are {age} years old")