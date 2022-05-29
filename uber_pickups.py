import streamlit as st          # To run the web application, I have chosen streamlit platform.
import pandas as pd             # Importing pandas and numpy to perform statistical analysis.
import numpy as np
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
st.title('Uber pickups in NYC')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz') # Using data stored in amazon aws cloud

@st.cache                                                      # @st.cache is used so that it stores data without loading every time we open web page.
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])      # Converting date time in the data sheet into required format.
    return data

data_load_state = st.text('Loading data...')
data = load_data(10000)                                        # Loading data for analysis.
data_load_state.text("Done! (using st.cache)")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')                                   # Providing a checkbox option, so that we can see the raw data on the web page.
    st.write(data)

st.subheader('Number of pickups by hour')
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)                                      # Creating a histogram of Number of pickups by hour.


hour_to_filter = st.slider('hour', 0, 23, 17)                  # Providing a slider option to choose particular hour in the range 0-23.
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

st.subheader('Map of all pickups at %s:00' % hour_to_filter)
st.map(filtered_data)                                          # Providing the pickup location of the vehicles on the map on a particular hour chosen in the slider. 

#/Users/abju/Documents/MS_project/uber_pickups.py  - This is the location where my file stored in my computer
#The follwing command is used to run the web application - streamlit run /Users/abju/Documents/MS_project/uber_pickups.py
