import streamlit as st
from datetime import datetime
import urllib.request
import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#ReaMe: To generate selected data to track,
#       run this program. it will download source data from OWI site
#       and write the selected data into a data consolidated file.


class SnaptoCursor(object):
    def __init__(self, ax, x, y):
        self.ax = ax
        self.ly = ax.axvline(color='k', alpha=0.2)  # the vert line
        self.lx = ax.axhline(color='k', alpha=0.2)  # the horiz line
        self.marker, = ax.plot([0],[0], marker="", color="crimson", zorder=3) 
        self.x = x
        self.y = y
        self.txt = ax.text(0.7, 0.9, '')

    def mouse_move(self, event):
        if not event.inaxes: return
        x, y = event.xdata, event.ydata
        #indx = np.searchsorted(self.x, [x])[0]
        #x = self.x[indx]
        #y = self.y[indx]
        self.ly.set_xdata(x) # disply vert line #<<<<<<
        self.lx.set_ydata(y)  # disply horiz line
        self.marker.set_data([x],[y]) #<<<<<<
        self.txt.set_text('x=%1.2f, y=%1.2f' % (x, y)) #<<<<<
        #self.txt.set_text('y=%1.2f' % y)
        self.txt.set_position((x-50,y)) #<<<<<<<
        #self.txt.set_position((0,y)) # disply set_text wrt x,y coord.
        self.ax.figure.canvas.draw_idle()

def plot_chart_1x(x_lst,y_lst,title=None,xlab=None,ylab=None, rc='21'): 
    r, c = int(rc[0]), int(rc[1])
    for m in range(len(x_lst)):
        loc = rc + str(m+1)
        x, y = x_lst[m], y_lst[m]
        fig, ax = plt.subplots(r,c, figsize=(9,5))
        ax.scatter(x, y)
        ax.set_title(title)
        ax.set_xlabel(xlab)
        ax.set_ylabel(ylab)
        ax.set_xticks(x[::40])
        ax.set_xticklabels(x[::40], rotation=30)

        plt.show(block=True)

def plot_chart_1(x_lst,y_lst,title=None,xlab=None,ylab=None, rc='11',ticks=5): 
    r, c = int(rc[0]), int(rc[1])
    for m in range(len(x_lst)):
        loc = rc + str(m+1)
        x, y = x_lst[m], y_lst[m]
        fig, ax = plt.subplots(r,c, figsize=(10,6))
        ax.scatter(x, y)
        ax.set_title(title)
        ax.set_xlabel(xlab)
        ax.set_ylabel(ylab)
        ax.set_xticks(x[::ticks]) #20]) # display selected x ticks
        ax.set_xticklabels(x[::ticks], rotation=30)
        
        ## cursor setup
        cursor = SnaptoCursor(ax, x, y)
        cid =  plt.connect('motion_notify_event', cursor.mouse_move)

        plt.grid()
        plt.show(block=True)

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
country_name = st.text_input('Enter country:')
st.write('Selected country is:', country_name)

# Download covid data from owid url
data, country_list = load_data(country_name) #('China')

if country_name not in country_list:
    st.warning('Oops...! Country not entered or not valid, please re-enter!')

# use a button to toggle country names
if st.checkbox('Show all country names'):
    check_raw_data(country_list, 'List of sorted country names:')
    
if st.checkbox('Raw data'):
    check_raw_data(data, 'Raw data of selected country')  

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
    ticks, country = freq, country_name

    ax[0].set_title(country)
    ax[0].set_xlabel('')
    ax[0].set_ylabel(y_label[0])
    ax[0].set_xticks(x1[::ticks])
    ax[0].set_xticklabels([]) #x1[::ticks], rotation=90, fontsize=8)
    ax[0].grid(linestyle='--')
    
    ax[1].set_xlabel('Date')
    ax[1].set_ylabel(y_label[1])
    ax[1].set_xticks(x1[::ticks])
    ax[1].set_xticklabels(x1[::ticks], rotation=90, fontsize=8)    
    ax[1].grid(linestyle='--')
    
    fig.tight_layout()
    st.pyplot(fig)

except:
    st.warning('Oops...! Please check if the country name is entered correctly.')
    

