#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')


# In[2]:


df = pd.read_csv('E:\Delete\Zomato/zomato.csv')


# In[3]:


df.head()


# In[4]:


df.isna().sum()


# In[5]:


df.dropna(axis='index', subset=['location'], inplace=True)


# In[6]:


df.isna().sum()


# In[7]:


len(df['location'].unique())


# In[8]:


locations = pd.DataFrame()


# In[9]:


locations['Name'] = df['location'].unique()


# In[10]:


locations.head()


# In[11]:


get_ipython().system('pip install geopy')


# In[12]:


from geopy.geocoders import Nominatim


# In[13]:


geolocator = Nominatim(user_agent = 'app')


# In[14]:


lat = []
lon = []
for location in locations['Name']:
    location = geolocator.geocode(location)
    if location is None:
        lat.append(np.nan)
        lon.append(np.nan)
    else:
        lat.append(location.latitude)
        lon.append(location.longitude)


# In[ ]:


locations['lat'] = lat
locations['lon'] = lon


# In[ ]:


locations.head()


# In[ ]:


locations.to_csv('E:\Delete\Zomato/zomato_location.csv', index=False)


# In[ ]:


Rest_locations = df['location'].value_counts().reset_index()


# In[ ]:


Rest_locations


# In[ ]:


Rest_locations.columns=['Name','count']
Rest_locations


# In[ ]:


Restaurant_locations = Rest_locations.merge(locations, on='Name', how='left').dropna()
Restaurant_locations.head()


# In[ ]:


get_ipython().system('pip install folium')


# In[ ]:


def generateBaseMap(default_location = [12.97, 77.59], default_zoom_start = 12):
    basemap = folium.Map(location=default_location, zoom_start = default_zoom_start)
    return basemap


# In[ ]:


import folium
basemap = generateBaseMap()
basemap


# In[ ]:


from folium.plugins import HeatMap


# In[ ]:


HeatMap(Restaurant_locations[['lat','lon', 'count']], zoom=20).add_to(basemap)


# In[ ]:


basemap


# In[ ]:


from folium.plugins import FastMarkerCluster


# In[ ]:


FastMarkerCluster(Restaurant_locations[['lat','lon','count']], zoom=20).add_to(basemap)


# In[ ]:


basemap


# In[ ]:


df['rate'].unique()


# In[ ]:


df.dropna(axis=0,subset=['rate'], inplace=True)


# In[ ]:


def split(x):
    return x.split('/')[0]


# In[ ]:


df.head()


# In[ ]:


df['rating'] = df['rate'].apply(split)


# In[ ]:


df.head()


# In[ ]:


df.replace('NEW',0, inplace=True)


# In[ ]:


df.replace('-',0, inplace=True)
df['rating'].unique()


# In[ ]:


df['rating'] = pd.to_numeric(df['rating'])


# In[ ]:


df.groupby('location')['rating'].mean()


# In[ ]:


df.groupby('location')['rating'].mean().sort_values()


# In[ ]:


avg_rating = df.groupby('location')['rating'].mean().sort_values(ascending=False).values


# In[ ]:


location = df.groupby('location')['rating'].mean().sort_values(ascending=False).index


# In[ ]:


location


# In[ ]:


rating = pd.DataFrame()


# In[ ]:


lat = []
lon = []
for place in location:
    place = geolocator.geocode(place)
    if place is None:
        lat.append(np.nan)
        lon.append(np.nan)
    else:
        lat.append(place.latitude)
        lon.append(place.longitude)


# In[ ]:


rating['location'] = location
rating['lat'] = lat
rating['long'] = lon
rating['avg_rating'] = avg_rating


# In[ ]:


rating.head()


# In[ ]:


rating.isna().sum()


# In[ ]:


rating.dropna(inplace = True)


# In[ ]:


rating[['lat','long','avg_rating']]


# In[ ]:


HeatMap(rating[['lat','long','avg_rating']]).add_to(basemap)


# In[ ]:


basemap


# In[ ]:


df.head()


# In[ ]:


filter = df['cuisines']=="North Indian"
df2 = df[filter]
df2.head()


# In[ ]:


df.group

