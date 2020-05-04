from operator import itemgetter
import pandas as pd
import numpy as np
from app.irsystem.models.BingImageSearchv7 import image_search
from app.data.name_data import names 

def get_top_n(topic, n, politicians, party, year):
    final_data = []
    if n:
        n=int(n)
    else:
        n=10
    debate_data = pd.read_csv('app/data/debate_transcripts_v5.csv')

    if not politicians and not topic:
        return []
    if not politicians:
        related_data = debate_data       
    else:
        politicians = [p.strip() for p in politicians.split(",")]
        input_politicians = []
        for politician in politicians:
            if politician in names.keys():
                for p in names[politician]:
                    input_politicians.append(p)
        input_politicians = set(input_politicians)
        if len(input_politicians) > 0:
            related_data = debate_data.loc[debate_data.speaker.isin(input_politicians)]
        else: 
            return []
    if party == "dm":
        related_data = related_data.loc[related_data.party.isin(["Democrat"])]
    elif party == "rp":
        related_data = related_data.loc[related_data.party.isin(["Republican"])]
    if year: 
        year_data = related_data.loc[related_data.debate_year.isin([year])]
        if not year_data.empty: 
            print('year data not empty')
            related_data = year_data
    if topic:        
        input = [topic.strip() for topic in topic.split(",")]
        topics = []
        topics += input
        for topic in input:
            words = topic.split(" ")
            if words[0] not in topics:
                topics.append(words[0])
        wc_matrix = np.zeros((len(topics), len(debate_data.index)))
        score_matrix = np.zeros((len(debate_data.index,)))
        for index, row in related_data.iterrows():
            speech = row['speech']
            column = wc_matrix[:,index]
            it = np.nditer(column, flags=['f_index'], op_flags=['readwrite'])
            while not it.finished:
                idx = it.index
                it[0] = speech.count(topics[idx])
                it.iternext()
            score_matrix[index] = np.sum(column)
        top_indices = (-score_matrix).argsort()[:n]
        for index in np.nditer(top_indices):
            score = score_matrix[index]
            if score > 0:
                trans_info = related_data.loc[index]
                debate_name = trans_info['debate_name']
                if 'Transcript:' in debate_name: 
                    debate_name.replace('Transcript:', '')
                obj = {"score": score_matrix[index], "debate_name": debate_name, "debate_date": trans_info['debate_date'], "speaker":trans_info['speaker'], "speech":trans_info['speech'], "link": trans_info["transcript_link"], "image":image_search(trans_info['speaker']), "party":trans_info['party']}
                final_data.append(obj)
        return final_data
    else:
        return []