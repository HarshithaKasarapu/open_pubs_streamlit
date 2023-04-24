import streamlit as st



import pandas as pd
import numpy as np
from PIL import Image
import plotly.express as px
import plotly.graph_objs as go
from scipy.spatial.distance import cdist

# Load the dataset
df = pd.read_csv("open_pubs.csv")

# Define the Streamlit app
def intro():
    st.markdown("<h1 style='color: #f0b1eb; font-size: 40px;'>Open Pubs</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style='color: #a950c7; font-size: 36px;'>If you can't be happy at least you can be drunk!</h1>", unsafe_allow_html=True)
    st.write("Life is not a fairytale. If you lose your shoe at midnight, you’re drunk !!")
    st.write("It’s strange how eight glasses of water a day seems impossible, but eight beers is so damn easy!!")
    image = Image.open('open_pubs_intro.jpg')
    st.image(image, '')

def dashboard():
    st.markdown("<h1 style='color: #8d51e0; font-size: 36px;'>Look where you'll have fun tonight!!</h1>", unsafe_allow_html=True)

    st.write("Glimpse where most of the pubs are:")
    top_regions = df["Region"].value_counts().head(5)
    image = Image.open('pubs_2.jpg')
    st.image(image, '')
    st.write("## Top 5 Regions by Pub Count")
    st.bar_chart(top_regions)
    num_pubs = df.groupby('Region')['name'].nunique().reset_index(name='Num Pubs')
    compact = pd.merge(df, num_pubs, on='Region')
    fig = px.scatter_mapbox(compact, lat="latitude", lon="longitude", hover_name="name",
                            hover_data={"Region": True, "Num Pubs": True},
                            size="Num Pubs", size_max=20, zoom=5,
                            mapbox_style="carto-positron")
    
    fig.update_layout(
    title="Choose Pubs from UK!!",
    mapbox=dict(
        
        center=dict(lat=54, lon=-2),
        zoom=5
    ),
    margin=dict(l=0, r=0, t=30, b=0)
)

    st.plotly_chart(fig, use_container_width=True)

def findbylocauth():
    st.title("Find your Local authority")
    image = Image.open('pubs.jpg')
    st.image(image, '')
    st.write("Select the Local Authority here to find pubs near you.")
    local_authorities = df["local_authority"].unique()
    selected_local_authority = st.selectbox("Select a local authority", local_authorities)
    columns_to_display = ["fsa_id", "name", "address",'Areaname'] 
    filtered_df = df[df["local_authority"] == selected_local_authority]
    st.table(filtered_df[columns_to_display])

def byareaname():
    st.title("Find your Area name")
    st.write("Select the Area name here to find pubs near you.")
    postal_code = df["Areaname"].unique()
    selected_Areaname= st.selectbox("Select an Area ", postal_code)
    columns_to_display = ["fsa_id", "name", "address",'local_authority' ,'postcode']
    filtered_df = df[df["Areaname"] == selected_Areaname]
    st.table(filtered_df[columns_to_display])



def bycoord():
    def euclidean_distance(lat1, lon1, lat2, lon2):
        return cdist([(lat1, lon1)], [(lat2, lon2)], metric='euclidean')[0][0]
    def find_nearest_pubs(latitude, longitude):
   
        distances = df.apply(lambda row: euclidean_distance(latitude, longitude, row['latitude'], row['longitude']), axis=1)
    
        df['distance'] = distances
    
        nearest_pubs = df.sort_values('distance').head(5)
   
        return nearest_pubs


    st.title('Find the nearest pubs by Latitudes and Longitudes')
    # Get the user's location
    image = Image.open('pubs_3.jpg')
    st.image(image, '')
    latitude = st.text_input('Enter your Latitude')
    longitude = st.text_input('Enter your Longitude')
    # Check if the user has entered their location
    if latitude and longitude:
        # Convert the latitude and longitude to floats
        latitude = float(latitude)
        longitude = float(longitude)
        # Find the 5 nearest pubs to the given location
        nearest_pubs = find_nearest_pubs(latitude, longitude)
        # Display the nearest pubs in a table
        st.write(nearest_pubs)
    



# Define the Streamlit app
def main():
    st.sidebar.title("Open Pubs Navigation")
    selection = st.sidebar.radio("Visit all for more Info",["Intro", "Dashboard", "By local authority", "By Area name", "Find by Co-ordinates"])
    # Show the appropriate page based on the user's selection
    if selection == "Intro":
        intro()
    elif selection == "Dashboard":
        dashboard()
    elif selection == "By local authority":
        findbylocauth()
    elif selection == "By Area name":
        byareaname()
    elif selection == "Find by Co-ordinates":
        bycoord()

    


# Run the app
if __name__ == "__main__":
    main()