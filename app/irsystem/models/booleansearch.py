#!/usr/bin/env python
# coding: utf-8

# ## This is some basic analysis of data
# So far I just roughly achieved the goal through basic boolean search. It is not very accurate. 
# <p>Input params: <strong>topic</strong>(required), <strong>number of results</strong>(optional, default=10), <strong>list of politicians</strong>(optional, default=null)</p>
# <p>Output items: the number of times the topic appears in the file, speaker of this paragraph, the speech content</p>
# <br/>This is just brief analysis, so it may take long time to get results (max: 16 seconds)

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# In[2]:


data = pd.read_csv('app/irsystem/data/debate_transcripts.csv')
data.head()


# In[3]:


import spacy
nlp = spacy.load("en_core_web_sm", disable=['parser', 'ner'])
random_state = 0

# Taking into consideration only nouns so as to identify the topics.
def only_nouns(texts):
    output = []
    for doc in nlp.pipe(texts):
        noun_text = " ".join(token.lemma_ for token in doc if token.pos_ == 'NOUN')
        output.append(noun_text)
    return output


# In[4]:


data_new = only_nouns(data["speech"])
speech_nouns = pd.DataFrame(data_new)
data["Index"] = data.index
speech_nouns["Index"] = speech_nouns.index
debate_data = pd.merge(data, speech_nouns, on="Index")
debate_data.columns = ["debate_name", "speaker", "speech_text", "index", "speech_nouns"]
debate_data = debate_data.drop(["index"], axis=1)
debate_data.head()


# In[5]:


# Dictionary of the debates.
debate_names = data["debate_name"]
number_of_debates = len(set(debate_names))
# print("Total number of democratic debates:", number_of_debates, "debates")

# Dictionary of name of speakers.
dem_speakers = data["speaker"]
number_of_speakers = len(set(dem_speakers))
# print("Total number of democratic speakers:",number_of_speakers, "speakers")


# In[6]:


# This is test code. Ignore this. 
num_arr = []
abSpeakers = []
for item in set(dem_speakers):
    split_arr = item.split(" ")
    split_arrs = item.split(".")
    if split_arr[0] == 'Speaker':
        num_arr.append(int(split_arr[1]))
    elif len(split_arrs) != 1 or len(split_arr[0])==1:
        abSpeakers.append(item)
    elif len(split_arr) > 1 and len(split_arr[1])==1:
        abSpeakers.append(item)
    elif len(split_arr) > 2 and len(split_arr[2])==1:
        abSpeakers.append(item)
# print(len(set(num_arr)))
# print(abSpeakers)


# In[7]:


# democrat_data = debate_data.loc[debate_data.speaker.isin({'Joe Biden', 'Elizabeth Warren', 'Bernie Sanders', 'Pete Buttigieg', 'Amy Klobuchar', 'Michael Bloomberg', 'Tom Steyer', 'Tulsi Gabbard','Donald Trump','Andrew Yang'})]
# democrat_data.speaker.value_counts()


# In[8]:


# bloom_data = democrat_data.loc[data.speaker=='Michael Bloomberg']
# bloom_data.head()


# In[16]:


import collections
from collections import Counter
from collections import defaultdict
from operator import itemgetter

def get_top_n_related(topic, n=10, politicians={}):
    new_dict = defaultdict(int)
    final_data = []
    if not politicians:
        related_data = debate_data       
    else:
        related_data = debate_data.loc[debate_data.speaker.isin(politicians)]
    for index, row in related_data.iterrows():
        word_dic = Counter(row["speech_text"].split(" "))
        if word_dic[topic] != 0:
            new_dict[index] = word_dic[topic]
    od = sorted(new_dict.items(), key=itemgetter(1), reverse=True)
    i=0
    for k, v in od: 
        obj = {"score": v, "debate": debate_data.loc[k]['debate_name'], "speaker":debate_data.loc[k]['speaker'], "speech_text":debate_data.loc[k]['speech_text']}
        final_data.append(obj)
        # print(v, debate_data.loc[k]['speaker']+"\n"+debate_data.loc[k]['speech_text'])
        # print(" ")
        i+=1
        if i==n:
            return final_data           


# In[17]:


# # Input example 1
# import time
# start_time = time.time()
# get_top_n_related("insurance", 5,  {"Donald Trump",'Joe Biden', 'Elizabeth Warren'})
# execution_time = time.time() - start_time
# # print("Excution time: " + str(execution_time))


# # In[18]:


# # input example 2
# start_time = time.time()
# get_top_n_related("insurance", 5)
# execution_time = time.time() - start_time
# # print("Excution time of example 2: " + str(execution_time))


# # In[20]:


# # input example 3
# start_time = time.time()
# get_top_n_related("insurance")
# execution_time = time.time() - start_time
# # print("Excution time of example 3: " + str(execution_time))

