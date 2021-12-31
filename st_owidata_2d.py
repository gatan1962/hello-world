import streamlit as st
from datetime import datetime
import urllib.request
import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests

#ReaMe: To generate selected data to track,
#       run this program. it will download source data from OWI site
#       and write the selected data into a data consolidated file.

def plot_chart(x_lst, y_lst, country, y_label, ticks=None):
    fig, ax = plt.subplots()
    ax.scatter(x_lst,y_lst)
    ax.set_xlabel('Date')
    ax.set_ylabel(y_label)
    plt.xticks(x_lst[::ticks], rotation=90, fontsize=8)
    plt.yticks(fontsize=10)
    plt.grid(linestyle='--')
    ax.set_title(country)
    return fig
    
######################################################
######## download data from OWI web-site  ############
######################################################
data_url = ('https://covid.ourworldindata.org/data/owid-covid-data.csv')

## To get latest data from data_url
r = requests.get(data_url)
st.write('Last update:', r.headers['Date'])

@st.cache
def load_data(country='Malaysia'):
    data = pd.read_csv(data_url, nrows=None)
    
    # change all columns string to lowercase
    lower_case = lambda x: str(x).lower()
    data.rename(lower_case, axis='columns', inplace=True)
    country_list = sorted(set(data['location']))
       
    # convert date from string to datetime
    data['date'] = pd.to_datetime(data['date']).dt.date
    # select country data of interest
    country_data = data[data['location'] == country]
    
    return country_data, country_list

def check_raw_data(input_data, header):
    st.subheader(header)
    st.write(input_data)

# program initialization
st.title('Covid-19 Trend Chart')
st.text('Data source:- https://covid.ourworldindata.org/data/owid-covid-data.csv')
# user input country name
#st.write('## Enter country:')
country_name = st.text_input('Enter country:')
country_name = " ".join(country_name.split()) # keep single space between components of name
st.write('Selected country is:', country_name)

# Download covid data from owid url
#data_load_status = st.write("Downloading covid data from owid in progress...")
data, country_list = load_data(country_name) #('China')

if country_name not in country_list:
    st.warning('Please enter country to continue...')

# use a button to toggle country names
#st.write(country_list)
if st.checkbox('Show all country names'):
    check_raw_data(country_list, 'List of sorted country names:')
    
if st.checkbox('Raw data'):
    check_raw_data(data, 'Raw data of selected country')  
#st.write(data.shape)
#st.write(data)


######################################################
######## 1. Define data of interest       ############
######################################################
y_label = ['new_cases', 'new_deaths']
x = data['date']
y_nc, y_nd = data[y_label[0]], data[y_label[1]]

##################################################################
######## 2. Generate chart with user select start date        ####
##################################################################
x_lst = list(x) # type: datetime

st.info('Slide to select Start Date:')
try:
    start_date = st.slider('', x_lst[0], x_lst[-1],\
                           format='YYYY/MM/DD') # use direct as datetime object
    date_index = x_lst.index(start_date)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
    x1 = x_lst[date_index:]
    y1 = y_nc[date_index:]
    y2 = y_nd[date_index:]
    freq = int(len(x1)//30) + 1

    fig, ax = plt.subplots(2, figsize=(8,6))
    ax[0].scatter(x1, y1)
    ax[1].scatter(x1, y2)
    #fig = plot_chart(x1, y1, country_name, ylabel, ticks=freq)
    
    ###---
    #ax.scatter(x_lst,y_lst)
    ticks, country = freq, country_name

    ax[0].set_title(country)
    ax[0].set_xlabel('')
    ax[0].set_ylabel(y_label[0])
    ax[0].set_xticks(x1[::ticks])
    ax[0].set_xticklabels([]) #x1[::ticks], rotation=90, fontsize=8)
    ax[0].grid(linestyle='--')
    #plt.yticks(fontsize=30)
    #ax[0].set_yticklabels(y1[::100],fontsize=20)
    
    ax[1].set_xlabel('Date')
    ax[1].set_ylabel(y_label[1])
    ax[1].set_xticks(x1[::ticks])
    ax[1].set_xticklabels(x1[::ticks], rotation=90, fontsize=8)    
    ax[1].grid(linestyle='--')
    
    #plt.xticks(x1[::ticks], rotation=90, fontsize=8)
    #plt.yticks(fontsize=10)
    #plt.grid(linestyle='--')
    
    ###---
    fig.tight_layout()
    st.pyplot(fig)

except:
    st.warning('Oops...! Please check if country is entered correctly.')
    

