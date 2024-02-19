#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# In[2]:


pd.read_csv(r'C:\Users\user\Documents\data folder/UScomments.csv',on_bad_lines='warn')


# In[4]:


comments=pd.read_csv(r'C:\Users\user\Documents\data folder/UScomments.csv',on_bad_lines='warn')


# In[5]:


comments.head()


# In[6]:


comments.isnull().sum()


# In[7]:


comments.dropna(inplace=True)


# In[8]:


comments.isnull().sum()


# In[9]:


#performing sentiment Analysis


# In[10]:


get_ipython().system('pip install textblob')


# In[11]:


from textblob import TextBlob


# In[12]:


comments.head(6)


# In[13]:


TextBlob("Logan Paul it's yo big day ‼️‼️‼️").sentiment


# In[14]:


TextBlob("Logan Paul it's yo big day ‼️‼️‼️").sentiment.polarity


# In[15]:


comments.shape


# In[16]:


sample_df = comments[0:1000]


# In[17]:


sample_df.shape


# In[18]:


polarity = []


for comment in comments['comment_text']:
    try:
        polarity.append(TextBlob(comment).sentiment.polarity)
    except:
        polarity.append(0)


# In[19]:


len(polarity)


# In[19]:


comments['polarity'] = polarity


# In[20]:


comments.head(5)


# In[21]:


#wordcloud Analysis of the data


# In[22]:


filter1 = comments['polarity']==1


# In[23]:


comments[filter1]


# In[24]:


comments_positive = comments[filter1]


# In[ ]:





# In[25]:


filter2 = comments['polarity']==-1


# In[26]:


comments[filter2]


# In[27]:


comments_negative = comments[filter2]


# In[28]:


comments_positive.head(5)


# In[29]:


get_ipython().system('pip install wordcloud')


# In[30]:


from wordcloud import WordCloud , STOPWORDS


# In[31]:


set(STOPWORDS)


# In[32]:


comments['comment_text']


# In[33]:


type(comments['comment_text'])


# In[34]:


' '.join(comments_positive['comment_text'])


# In[35]:


total_comments_positive = ' '.join(comments_positive['comment_text'])


# In[36]:


wordcloud = WordCloud(stopwords=set(STOPWORDS)).generate(total_comments_positive)


# In[37]:


plt.imshow(wordcloud)
plt.axis('off')


# In[38]:


total_comments_negative = ' '.join(comments_negative['comment_text'])


# In[39]:


wordcloud2 = WordCloud(stopwords=set(STOPWORDS)).generate(total_comments_negative)


# In[40]:


plt.imshow(wordcloud2)
plt.axis('off')


# In[41]:


#performing Emoji's Analysis


# In[42]:


get_ipython().system('pip install emoji==2.2.0')


# In[43]:


import emoji


# In[44]:


emoji.__version__


# In[45]:


comments['comment_text'].head(6)


# In[46]:


comment = 'trending 😉'


# In[47]:


[char for char in comment if char in emoji.EMOJI_DATA]


# In[48]:


emoji_list = []

for char in comment:
        if char in emoji.EMOJI_DATA:
            emoji_list.append(char)


# In[49]:


emoji_list


# In[50]:


all_emojis_list = []

for comment in comments['comment_text'].dropna():
    for char in comment:
        if char in emoji.EMOJI_DATA:
            all_emojis_list.append(char)


# In[51]:


all_emojis_list[0:10]


# In[52]:


from collections import Counter


# In[53]:


Counter(all_emojis_list).most_common(10)


# In[54]:


Counter(all_emojis_list).most_common(10)[0]


# In[55]:


Counter(all_emojis_list).most_common(10)[0][0]


# In[56]:


emojis = [Counter(all_emojis_list).most_common(10)[i][0] for i in range(10)]


# In[57]:


Counter(all_emojis_list).most_common(10)[2][0]


# In[58]:


Counter(all_emojis_list).most_common(10)[1][1]


# In[59]:


freqs = [Counter(all_emojis_list).most_common(10)[i][1] for i in range(10)]


# In[60]:


freqs


# In[61]:


import plotly.graph_objs as go
from plotly.offline import iplot


# In[62]:


trace = go.Bar(x=emojis, y=freqs)


# In[65]:


iplot([trace])


# In[63]:


#collecting the entire data of youtube


# In[66]:


import os


# In[69]:


files=os.listdir(r'C:\Users\user\Documents\data folder\additional_data-20240218T072907Z-001\additional_data')


# In[70]:


files


# In[72]:


files_csv = [file for file in files if '.csv' in file]


# In[73]:


files_csv


# In[80]:


full_df = pd.DataFrame()
path = r'C:\Users\user\Documents\data folder\additional_data-20240218T072907Z-001\additional_data'

for file in files_csv:
    current_df = pd.read_csv(path+'/'+file , encoding='iso-8859-1')
    
    full_df = pd.concat([full_df , current_df] , ignore_index=True)


# In[81]:


full_df.shape


# In[88]:


#which of the  category having  maximum likes


# In[89]:


full_df.head(5)


# In[90]:


full_df['category_id'].unique()


# In[94]:


json_df = pd.read_json(r'C:\Users\user\Documents\data folder\additional_data-20240218T072907Z-001\additional_data/US_category_id.json')


# In[95]:


json_df


# In[97]:


json_df['items'][0]


# In[98]:


json_df['items'][1]


# In[105]:


cat_dict = {}
 
for item in json_df['items'].values:
 cat_dict[int(item['id'])] = item['snippet']['title']


# In[106]:


cat_dict


# In[108]:


full_df['category_name'] = full_df['category_id'].map(cat_dict)


# In[110]:


full_df.head(4)


# In[115]:


plt.figure(figsize=(12,8))
sns.boxplot(x='category_name' , y='likes' , data=full_df)
plt.xticks(rotation='vertical')


# In[116]:


#finding out whether audience is engaged or not(like rate, dislike rate and comment count)


# In[119]:


full_df['like_rate'] = (full_df['likes']/full_df['views'])*100
full_df['dislike_rate'] = (full_df['dislikes']/full_df['views'])*100
full_df['comment_count_rate'] = (full_df['comment_count']/full_df['views'])*100


# In[120]:


full_df.columns


# In[124]:


plt.figure(figsize=(8,6))
sns.boxplot(x='category_name' , y='like_rate' , data=full_df)
plt.xticks(rotation='vertical')
plt.show()


# In[125]:


sns.regplot(x='views' , y='likes' , data = full_df)


# In[126]:


full_df.columns


# In[128]:


full_df[['views', 'likes', 'dislikes']].corr()


# In[131]:


sns.heatmap(full_df[['views', 'likes', 'dislikes']].corr(), annot=True)


# In[132]:


#which channels have the larger number of trending videos


# In[133]:


full_df.head(6)


# In[134]:


full_df['channel_title'].value_counts()


# In[135]:


cdf = full_df.groupby(['channel_title']).size().sort_values(ascending=False).reset_index()


# In[138]:


cdf = cdf.rename(columns={0:'total_videos'})


# In[139]:


cdf


# In[147]:


import plotly.express as px


# In[151]:


px.bar(data_frame=cdf[0:20] , x='channel_title' , y='total_videos')

