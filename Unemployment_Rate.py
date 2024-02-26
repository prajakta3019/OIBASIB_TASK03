#!/usr/bin/env python
# coding: utf-8

# In[ ]:


Name : Prajakta Ramesh Chavan.
Date:23/02/2024
Domain: Data Science -oasis Infobyte 
Task no:02: Unemployment analysis with Python


# In[1]:


#importing the necessary libraries
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

import calendar

import datetime as dt

import plotly.io as pio
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from IPython.display import HTML


# In[2]:


df = pd.read_csv(r'C:\Users\Dell\Desktop\dataset\Unemployment_Rate.csv')
df


# In[39]:


india = pd.read_csv(r'C:\Users\Dell\Desktop\dataset\Unemployment_in_India.csv')
india


# In[ ]:


india.head(5)


# In[3]:


df.head(5)


# In[4]:


df.shape


# In[40]:


india.shape


# In[5]:


df.info()


# In[41]:


india.info()


# In[6]:


df.isnull().sum()


# In[7]:


df.describe()


# In[42]:


india.describe()


# In[8]:


df.duplicated().sum()


# In[43]:


india.duplicated().sum()


# In[9]:


df.columns =['States','Date','Frequency','Estimated Unemployment Rate','Estimated Employed','Estimated Labour Participation Rate','Region','longitude','latitude']


# In[10]:


df.columns


# In[44]:


india.columns =['States','Date','Frequency','Estimated Unemployment Rate','Estimated Employed','Estimated Labour Participation Rate','Area']


# In[45]:


india.columns


# In[11]:


df.head(2)


# In[46]:


india.head(2)


# In[12]:


df['Date'] = pd.to_datetime(df['Date'],dayfirst=True)


# In[13]:


df['Frequency']= df['Frequency'].astype('category')


# In[14]:


df['Month'] =  df['Date'].dt.month


# In[15]:


df['MonthNumber'] = df['Month'].apply(lambda x : int(x))


# In[16]:


df['MonthName'] =  df['MonthNumber'].apply(lambda x: calendar.month_abbr[x])


# In[17]:


df['Region'] = df['Region'].astype('category')


# In[18]:


df.drop(columns='Month',inplace=True)


# In[19]:


df.describe()


# In[20]:


round(df[['Estimated Unemployment Rate', 'Estimated Employed', 'Estimated Labour Participation Rate']].describe().T,2)


# In[21]:


regionStats = df.groupby(['Region'])[['Estimated Unemployment Rate',
                                      'Estimated Employed',
                                      'Estimated Labour Participation Rate']].mean().reset_index()

round(regionStats,2)


# In[22]:


heatMap = df[['Estimated Unemployment Rate', 'Estimated Employed', 
              'Estimated Labour Participation Rate', 'longitude', 'latitude', 'MonthNumber']]

heatMap = heatMap.corr()

plt.figure(figsize=(23,8))
sns.heatmap(heatMap, annot=True,cmap='magma', fmt='.3f', linewidths=1)
plt.title('heatMap')
plt.show()


# In[37]:


fig = px.box(
    df,
    x='States',
    y='Estimated Unemployment Rate',
    color='States',
    title='unemploymentRate',
    template='plotly'
)
fig.show()


# In[23]:


#plotting a "Bar-plot" to find the "average unemployment rate in each state"
newDF = df[['Estimated Unemployment Rate','States']]

#grouping the dataframe by 'States' and finding the corresponding 'mean'
newDF = newDF.groupby('States').mean().reset_index()

#sorting the values in the dataframe
newDF = newDF.sort_values('Estimated Unemployment Rate')

fig = px.bar(newDF, 
             x='States',
             y='Estimated Unemployment Rate',
             color='States',
             title='State-wise Average Employment Rate')
fig.show()


# In[24]:


fig = px.bar(df, 
             x='Region',
             y='Estimated Unemployment Rate',
             animation_frame = 'MonthName',
             color='States',
             title='Region-wise Unemployment Rate',
             height=800)

fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1500

fig.show()


# In[25]:


unempDF = df[['States','Region','Estimated Unemployment Rate','Estimated Employed','Estimated Labour Participation Rate']]

unempDF = unempDF.groupby(['Region','States'])['Estimated Unemployment Rate'].mean().reset_index()

#printing the new dataframe
unempDF.head(4)


# In[26]:


fig = px.sunburst(unempDF, 
                  path=['Region','States'], 
                  values='Estimated Unemployment Rate',
                  title= 'unemployment rate in each region and state',
                  height=650)
fig.show()


# In[27]:


#!pip install  sunburst


# In[28]:


fig = px.scatter_geo(df,'longitude', 'latitude', 
                     color="Region",
                     hover_name="States", 
                     size="Estimated Unemployment Rate",
                     animation_frame="MonthName",
                     scope='asia',
                     title='Lockdown Impact throughout India')

fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1200

#updating the geospatial axes ranges and ocean color
fig.update_geos(lataxis_range=[5,35], 
                lonaxis_range=[65, 100],
                oceancolor="#6dd5ed",
                showocean=True)

fig.show()


# In[29]:


df47 = df[(df['MonthNumber'] >= 4) & (df['MonthNumber'] <=7)]

#filtering dataset between month 1 and 4 (inclusive) - before lockdown
df14 = df[(df['MonthNumber'] >= 1) & (df['MonthNumber'] <=4)]


# In[30]:


df47g = df47.groupby('States')['Estimated Unemployment Rate'].mean().reset_index()

#grouping the dataframe on the basis of "States" and finding the corresponding mean values
df14g = df14.groupby('States')['Estimated Unemployment Rate'].mean().reset_index()

#clubbing the 2 dataframe values
df47g['Unemployment Rate before lockdown'] = df14g['Estimated Unemployment Rate']

#renaming the column values for better understanding
df47g.columns = ['States','unemploymentRate A/ lockdown','unemploymentRate B/ lockdown']

#displaying the top results
df47g.head()


# In[31]:


df47g['% change in unemployment'] = round(df47g['unemploymentRate A/ lockdown'] - df47g['unemploymentRate B/ lockdown']/df47g['unemploymentRate B/ lockdown'],2)


# In[32]:


df47g = df47g.sort_values('% change in unemployment')


# In[33]:


fig = px.bar(df47g, x='States',y='% change in unemployment',
             color='% change in unemployment',
             title='% change in Unemployment A/ Lockdown')



# In[34]:


def sort_impact(x):
    if x <= 10:
        #impactedState
        return ''
    
    elif x <= 20:
        #hardImpactedState
        return ''
    
    elif x <= 30:
        #harderImpactedState
        return ''
    
    elif x <= 40:
        #hardestImpactedState
        return ''
    
    return x    


# In[35]:


df47g['impactStatus'] = df47g['% change in unemployment'].apply(lambda x:sort_impact(x))


# In[36]:


fig = px.bar(df47g, 
             y='States',
             x='% change in unemployment',
             color='impactStatus',
             title='Lockdown Impact on Employment in India')

fig.show()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




