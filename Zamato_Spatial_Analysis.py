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


# In[15]:


locations['lat'] = lat
locations['lon'] = lon


# In[16]:


locations.head()


# In[17]:


locations.to_csv('E:\Delete\Zomato/zomato_location.csv', index=False)


# In[18]:


Rest_locations = df['location'].value_counts().reset_index()


# In[19]:


Rest_locations


# In[20]:


Rest_locations.columns=['Name','count']
Rest_locations


# In[21]:


Restaurant_locations = Rest_locations.merge(locations, on='Name', how='left').dropna()
Restaurant_locations.head()


# In[22]:


get_ipython().system('pip install folium')


# In[23]:


def generateBaseMap(default_location = [12.97, 77.59], default_zoom_start = 12):
    basemap = folium.Map(location=default_location, zoom_start = default_zoom_start)
    return basemap


# In[24]:


import folium
basemap = generateBaseMap()
basemap


# In[25]:


from folium.plugins import HeatMap


# In[26]:


HeatMap(Restaurant_locations[['lat','lon', 'count']], zoom=20).add_to(basemap)


# In[27]:


basemap


# In[28]:


from folium.plugins import FastMarkerCluster


# In[29]:


FastMarkerCluster(Restaurant_locations[['lat','lon','count']], zoom=20).add_to(basemap)


# In[30]:


basemap


# In[31]:


df['rate'].unique()


# In[32]:


df.dropna(axis=0,subset=['rate'], inplace=True)


# In[33]:


def split(x):
    return x.split('/')[0]


# In[34]:


df.head()


# In[35]:


df['rating'] = df['rate'].apply(split)


# In[36]:


df.head()


# In[37]:


df.replace('NEW',0, inplace=True)


# In[38]:


df.replace('-',0, inplace=True)
df['rating'].unique()


# In[39]:


df['rating'] = pd.to_numeric(df['rating'])


# In[40]:


df.groupby('location')['rating'].mean()


# In[41]:


df.groupby('location')['rating'].mean().sort_values()


# In[42]:


avg_rating = df.groupby('location')['rating'].mean().sort_values(ascending=False).values


# In[43]:


location = df.groupby('location')['rating'].mean().sort_values(ascending=False).index


# In[44]:


location


# In[45]:


rating = pd.DataFrame()


# In[46]:


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


# In[47]:


rating['location'] = location
rating['lat'] = lat
rating['long'] = lon
rating['avg_rating'] = avg_rating


# In[48]:


rating.head()


# In[49]:


rating.isna().sum()


# In[50]:


rating.dropna(inplace = True)


# In[51]:


rating[['lat','long','avg_rating']]


# In[52]:


HeatMap(rating[['lat','long','avg_rating']]).add_to(basemap)


# In[53]:


basemap


# In[54]:


df.head()


# In[55]:


filter = df['cuisines']=="North Indian"
df2 = df[filter]
df2.head()


# In[58]:


df2.groupby('location')['url'].count()


# In[59]:


df2.groupby('location')['url'].count().reset_index()


# In[65]:


north_india = df2.groupby('location')['url'].count().reset_index()
north_india.columns = ['Name', 'count']
north_india


# In[70]:


north_india=north_india.merge(locations, on='Name', how='left').dropna()


# In[68]:


north_india


# In[71]:


north_india[['lat','lon','count']]


# In[72]:


HeatMap(north_india[['lat','lon','count']], zoom=20, radius=15).add_to(basemap)


# In[73]:


basemap


# In[74]:


def Heatmap_zone(zone):
    df2 = df[df['cuisines']==zone]
    df_zone = df2.groupby('location')['url'].count().reset_index()
    df_zone.columns = ['Name','count']
    df_zone = df_zone.merge(locations, on='Name', how='left').dropna()
    HeatMap(df_zone[['lat','lon','count']],zoom=20,radius=15).add_to(basemap)
    return basemap


# In[77]:


Heatmap_zone('Italian')


# In[ ]:




