# coding: utf-8

from PIL.Image import new
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pydeck as pdk
import streamlit as st

plt.rc('axes', titlesize=12, labelsize=8)
plt.rc('xtick', labelsize=8)
plt.rc('ytick', labelsize=8)

# Magic markdown usage
"""# Welcome to price mapping!"""

# Another markdown usage, useful for line breaking and keeping neatness
st.markdown("#### Lots of information on properties with a quick glimpse!"
            " Load the dataset and get the analysis. Hover over the properties"
            " on the map for more info. Click the '?' for tips!")
st.markdown("---")
"""Click the '+' to expand the sections you want to look."""
# Creates an expander element where a .csv file is uploaded
with st.expander('Load your .csv data file here!', expanded=True):
  data_file = st.file_uploader("Pick your file", type=[".csv"])

# Loads a .csv into a dataframe. Limits the columns and formats them.
def load_mapping_df():
  data = pd.read_csv(data_file, decimal=",",
                     usecols=['Property_ID', 'Price', 'Longitude', 'Latitude'])
  format_mapping={'Property_ID': '{:.0f}',
                  'Price': 'R$ {:,.2f}',
                  'Longitude': '{:,.2f}'}
  # for key, value in format_mapping.items():
  #   data[key] = data[key].apply(value.format)
  # data['Property_ID'] = data['Property_ID'].astype(int)
  data['Price'] = data['Price'].astype(float).round(2)
  data['Latitude'] = data['Latitude'].astype(float).round(6)
  data['Longitude'] = data['Longitude'].astype(float).round(6)
  return data

# Saves dataframe into a variable and drops rows containing '<NA>'
# since every column has absolute priority.
main_df = load_mapping_df()
no_na_df = main_df.dropna()
# IMPORTANT! FORMAT!!
# st.write(no_na_df.style.format({'Price': "R$ {:,.2f}"}))

# Begins a portion of code concerning an 'expander' element
with st.expander('Dataframe information'):
  # Definition of three columns and subsequent column content
  c1, c2, c3 = st.columns([1.5,2,3])
  with c1:
    st.metric(label="Number or properties", value=len(main_df['Property_ID']))
  with c2:
    st.metric("Properties missing coordinates",
              int(max(main_df['Latitude'].isna().sum(),
                      main_df['Latitude'].isna().sum())))
  with c3:
    avg = main_df['Price'].mean()
    st.metric('Average price', f"R$ {avg:,.2f}")
 
  # Create a matplotlib figure and set it's dimensions (in inches)
  price_histogram = plt.figure(figsize=(6, 3))
  # Generate axis and set properties
  ax1 = price_histogram.add_axes([0, 0, 1, 1])
  ax1.set(title='Price histogram', xlabel='Prices (R$ x1000)', ylabel='Number of properties')
  ax1.xaxis.set_major_locator(MultipleLocator(100))
  ax1.xaxis.set_minor_locator(MultipleLocator(50))
  # ax1.tick_params(which='minor', length=4, color='r')
  prices = main_df['Price']/1000
  hist_classes = 40
  plt.grid(True)
  ax1.hist(prices, hist_classes, facecolor='darkcyan', alpha=0.5)
  
  # price_histogram, ax1 = plt.subplots()

  st.pyplot(price_histogram)
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

def price_to_color_coding():
  bins = [200000, 320000, 440000, 580000, 700000, 820000, 1000000, np.inf]  
  colors = {"red": '(255,45,0)', "orange": '(255,165,0)', "yellow":'(245,255,0)',
            "green": '(50,255,0)', "cyan": '(0,235,255)', "blue": '(0,10,255)',
            "violet": '(230,0,255)'}
  no_na_df['Color'] = pd.cut(no_na_df['Price'],bins,labels=colors)
  no_na_df['Color'] = no_na_df['Color'].replace(colors)
  c_red = []
  c_green = []
  c_blue = []
  for each_color in list(no_na_df['Color']):
    components = each_color.split(',')
    c_red.append(components[0].split('(')[1])
    c_green.append(components[1])
    c_blue.append(components[2].split(')')[0])
  no_na_df['Red'] = [int(x) for x in c_red]
  no_na_df['Green'] = [int(x) for x in c_green]
  no_na_df['Blue'] = [int(x) for x in c_blue]
  no_na_df.drop('Color', axis=1, inplace=True)
  
price_to_color_coding()

def radius():
  return 8

with st.expander('City map', expanded=True):
# Draws map
  st.pydeck_chart(pdk.Deck(
      map_provider = "mapbox",
      map_style = pdk.map_styles.ROAD,
      initial_view_state=pdk.ViewState(
          latitude=mean_latitude,
          longitude=mean_longitude,
          bearing=0,
          zoom=15,
          min_zoom=13,
          max_zoom=17,
          pitch=60,
      ),
      layers=[
        pdk.Layer(
          'ColumnLayer',
          data=no_na_df,
          get_position='[Longitude, Latitude]',
          get_elevation='[Price]',
          radius=radius(),
          elevation_scale=0.0005,
          get_fill_color=['Red','Green','Blue',125],
          auto_highlight=True,
          pickable=True,
        ),
      ],
      tooltip = {
      "html": "ID: <i>{Property_ID}</i><br/> R$ <b>{Price}</b>",
      "style": {"background": "blue", "color": "white", "font-family": '"Helvetica Neue", Arial', "z-index": "10"},
      }
    )
  )

