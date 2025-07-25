import streamlit as st
import pandas as pd
import numpy as np
st.title('Uber pickups in NYC')
DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
          'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data
# Create a text element and let the reader know the data is lclearoading.
data_load_state = st.text('Loading data...')
# Load 10,000 rstreamlit helloows of data into the dataframe.
# Notify the reader that the data was successfully loaded.
data = load_data(1000)
data_load_state.text('Loading data...done!')
print("Hello1 here  World!")