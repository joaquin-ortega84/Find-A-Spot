import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import geopandas as gpd
import plotly.io as pio


st.title('Find-A-Spot')
st.subheader('Rental prices in Barcelona by neighborhood')
st.write('Compare the average monthly rental price between neighborhoods in Barcelona')

# Map 1 - Prices per month
df = pd.read_csv('../CSV clean/precios_clean.csv')

# Load GeoJSON file
geojson_file = "/Users/joaquinortega/code/joaquin-ortega84/Find-A-Spot/Data/barris.geojson"
gdf = gpd.read_file(geojson_file)

# Load data from CSV file
# Merge GeoJSON and CSV data based on a common column
merged_df = gdf.merge(df, left_on='NOM', right_on='NOM', how='left')

# Create the choropleth map with customized tooltip
fig = px.choropleth(
    merged_df,
    geojson=merged_df.geometry,
    locations=merged_df.index,
    color='2011',
    labels={'2011': 'Price/month'},
    color_continuous_scale='purd',
    range_color=(merged_df['2011'].min(), merged_df['2011'].max()),
    hover_data={'NOM': True}
)

# Update the map layout
fig.update_geos(projection_type='orthographic', fitbounds="locations", visible=False)
fig.update_layout(
    geo=dict(showframe=False, showcoastlines=False),
    margin=dict(l=0, r=0, t=0, b=0),  # Adjust the margin values as desired
    title_font_size=20  # Adjust the font size of the title as desired
)

# Display the map using Streamlit
st.plotly_chart(fig)

st.markdown('---')

st.subheader('Local stores in Barcelona by activity segment')
st.write('Browse the locations and concentration of different types of local stores in Barcelona')

# Assuming you have 'censo_df' DataFrame with the required data
censo_df = pd.read_csv('/Users/joaquinortega/code/joaquin-ortega84/Find-A-Spot/Data/CSV clean/english_censo_clean.csv')
map_censo_df = pd.DataFrame(censo_df[['Name of Activity','Latitud','Longitud']])

# Get unique names in the 'Name of Activity' column
unique_names = censo_df['Name of Activity'].unique()

# Create scatter mapbox figure
fig = go.Figure()

# Add traces for each unique name
for name in unique_names:
    df_subset = censo_df[censo_df['Name of Activity'] == name]
    fig.add_trace(go.Scattermapbox(
        lat=df_subset['Latitud'],
        lon=df_subset['Longitud'],
        mode='markers',
        marker=dict(color='fuchsia'),
        hovertext=df_subset['Name of Activity'],
        name=name
    ))

# Set mapbox style
fig.update_layout(mapbox_style="open-street-map")

# Set initial center coordinates and zoom level
fig.update_layout(
    mapbox=dict(
        center=dict(lat=41.387, lon=2.170),
        zoom=10
    )
)

# Set layout margins and width
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, width=800)

# Create dropdown menu
updatemenu = []
buttons = []
for name in unique_names:
    visible = [False] * len(unique_names)
    visible[unique_names.tolist().index(name)] = True

    button = dict(label=name,
                  method="update",
                  args=[{"visible": [name == trace.name for trace in fig.data]}])
    buttons.append(button)

updatemenu = list([
    dict(active=0,
         buttons=list(buttons),
         x=0.1,  # Adjust the x position of the dropdown menu
         y=0.95,  # Adjust the y position of the dropdown menu
         xanchor='left',
         yanchor='top'
         )
])

fig.update_layout(showlegend=False, updatemenus=updatemenu)

# Show the figure
st.plotly_chart(fig)
