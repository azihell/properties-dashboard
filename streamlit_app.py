# coding: utf-8

from numpy import e, integer
import streamlit as st
import pandas as pd
import pydeck as pdk

# Magic markdown usage
"""# Welcome to price mapping!"""

# Another markdown usage, useful for line breaking and keeping neatness
st.markdown("#### Lots of information on properties with a quick glimpse!"
            " Load the dataset and get the analysis. Hover over the properties"
            " on the map for more info. Click the '?' for tips!")
st.markdown("---")
"""Click the '+' to expand the sections and perform the data analysis."""
# Creates an expander element where a .csv file is uploaded
with st.expander('Load your .csv data file here!', expanded=True):
  img_file_buffer = st.file_uploader("Pick your file", type=[".csv"])

# Loads a .csv into a dataframe. Limits the columns and formats them.
def load_mapping_df():
  data = pd.read_csv(img_file_buffer, decimal=',',
                     usecols=['Property_ID', 'Price', 'Longitude', 'Latitude'])
  data['Price'] = data['Price'].astype(float).round(2)
  data['Latitude'] = data['Latitude'].astype(float).round(6)
  data['Longitude'] = data['Longitude'].astype(float).round(6)
  return data

# Saves dataframe into a variable and drops rows containing '<NA>'
# since every column has absolute priority.
main_df = load_mapping_df()
main_df.style.format(precision=2, na_rep='--', thousands=":.")
no_na_df = main_df.dropna()

# Prints dataframe on the app
st.write(main_df)

# Begins a portion of code concerning an 'expander' element
with st.expander('Dataframe information'):
  # Definition of three columns and subsequent column content
  c1, c2, c3 = st.columns([1.5,2,2])
  with c1:
    st.metric(label="Number or properties", value=len(main_df['Property_ID']))
  with c2:
    st.metric("Properties missing coordinates",
              int(max(main_df['Latitude'].isna().sum(),
                      main_df['Latitude'].isna().sum())))
  with c3:
    st.metric('Average price (R$)', main_df['Price'].mean().round(2))

# Mean coordinates that are used to center the properties on the map  
mean_longitude = no_na_df['Longitude'].mean().round(6)
mean_latitude = no_na_df['Latitude'].mean().round(6)

# Begins a portion of code concerning the sidebar. Can be appended later on thanks to "with" usage.
with st.sidebar:
  st.subheader('Price range slider')
  filter_slider = st.slider('R$ x1.000', min(no_na_df['Price'])/1000,
                            max(no_na_df['Price'])/1000,
                            (min(no_na_df['Price'])/1000,
                             max(no_na_df['Price'])/1000), step=10.0,
                            key='filter_slider',
                            help='Maximum and minimum values were based on **.csv** data.')
  lowest_price = filter_slider[0]
  highest_price = filter_slider[1]

# Limits the dataframe according to the Prices slider
no_na_df = no_na_df[(no_na_df.Price >= lowest_price*1000) &
              (no_na_df.Price <= highest_price*1000)]

# Draws map
st.pydeck_chart(pdk.Deck(
    map_provider = "mapbox",
    map_style = pdk.map_styles.ROAD,
    initial_view_state=pdk.ViewState(
        latitude=mean_latitude,
        longitude=mean_longitude,
        # view_proportion = 0.8,
        zoom=15,
        min_zoom=13,
        max_zoom=17,
        pitch=50,
    ),
    layers=[
      pdk.Layer(
        'ColumnLayer',
        data=no_na_df,
        get_position='[Longitude, Latitude]',
        get_elevation='[Price]',
        radius=5,
        elevation_scale=0.0005,
        get_fill_color=[48, 128, 255, 255],
        auto_highlight=True,
        pickable=True,
      ),
    ],
    tooltip = {
    "html": "ID: <i>{Property_ID}</i><br/> R$ <b>{Price}</b>",
    "style": {"background": "blue", "color": "white", "font-family": '"Helvetica Neue", Arial', "z-index": "10"},
}
))
