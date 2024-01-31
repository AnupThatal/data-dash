import streamlit as st
import pandas as pd
import folium
from folium import plugins
from streamlit_folium import st_folium


df = pd.read_csv('df_final.csv')
df1=pd.read_csv('HHC_Data.csv')

# Sidebar
with st.sidebar:
    
    location=df1['ward number'].unique().tolist()
    location_area=st.selectbox('Select location',location)
    areas_list = df['b10_sub_dmi'].dropna().unique().tolist()
    selected_area = st.selectbox('Select Area', areas_list)
    if selected_area:
        filtered_df = df[df['b10_sub_dmi'] == selected_area]
        filtered_location_df=df1[df1['Areas']==location_area]
        P=filtered_location_df['Packages']
        SDMA=filtered_location_df['sDMA']
        ward=filtered_location_df['ward number']
        mun=filtered_location_df['District'][0]
        print(mun)
        packages = filtered_df['gb10-b10_package']
        person=filtered_df['Person']
        phone=filtered_df['Phone']
        sub_dmi_counts = filtered_df['b10_sub_dmi'].value_counts()
        st.write(f"Municipality :blue[{mun}]")
        st.write(f"ward of that areas :blue[{ward}]")
        st.write(f'Packages of :blue[{packages}]')
        st.write(f"ward of :blue[{SDMA}]")
        st.write(f'Person responsible :blue[{person}]')
        st.write(f'Phone number of that person :blue[{phone}]')
        st.write(sub_dmi_counts)

# Main content
col1, = st.columns(1)  # Note the use of comma to unpack the list

with col1:
    if selected_area:
        # Filter DataFrame for selected area
        selected_df = df[df['b10_sub_dmi'] == selected_area]

        # Drop rows with NaN values in location coordinates
        selected_df = selected_df.dropna(subset=['b02-Latitude', 'b02-Longitude'])

        # Extract latitude and longitude lists
        lat = selected_df['b02-Latitude'].astype(float).tolist()
        lon = selected_df['b02-Longitude'].astype(float).tolist()

        # Calculate the center of the map
        center_lat = sum(lat) / len(lat) if len(lat) > 0 else 0
        center_lon = sum(lon) / len(lon) if len(lon) > 0 else 0

        # Create a Folium map centered at the mean of coordinates
        folium_map = folium.Map(location=[center_lat, center_lon], zoom_start=16)

        # Add markers for each location with smaller icon
        for i in range(len(lat)):
            folium.Marker([lat[i], lon[i]], icon=folium.Icon(icon="circle", prefix='fa', icon_color='blue', icon_size=(2,2))).add_to(folium_map)

        # Display the Folium map using streamlit_folium
        st_folium(folium_map,width=1000, height=500)
