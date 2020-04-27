from operator import itemgetter
import pandas as pd
import spacy
import numpy as np
from app.irsystem.models.BingImageSearchv7 import image_search

nlp = spacy.load('en_core_web_lg')
vocab = [w for w in nlp.vocab if w.is_lower and w.prob >= -15 and w.vector.any()]
vocab_vectors = np.array([w.vector for w in vocab])

def most_similar_by_embedding(word_vector, top=4):
    sim = np.inner(word_vector, vocab_vectors)
    by_similarity = [vocab[i] for i in np.argsort(-sim)]
    top_similar = by_similarity[:top]
    return [w.lower_ for w in top_similar]

def most_similar(word: str, top=4):
    words = word.split(" ")
    output = []
    for word in words:
        word = word.strip()
        word_vector = nlp.vocab[word].vector
        if not np.any(word_vector):
            return [word]
        most_sim = most_similar_by_embedding(word_vector, top)
        most_sim.remove(word)
        output += most_sim
    return output

def get_top_n_related(topic, n, politicians={}):
    if n:
        n=int(n)
    else:
        n=10
    debate_data = pd.read_csv('app/data/debate_transcripts_v5.csv')
    final_data = []
    if not politicians and not topic:
        return
    if not politicians:
        related_data = debate_data       
    else:
        politicians = [p.strip() for p in politicians.split(",")]
        input_politicians = []
        for politician in politicians:
            item = politician.split()
            word=""
            for name in item:
                word += name.capitalize() + " "
            input_politicians.append(word.strip())
        input_politicians = set(input_politicians)
        related_data = debate_data.loc[debate_data.speaker.isin(input_politicians)]
    if topic:        
        input = [topic.strip() for topic in topic.split(",")]
        topics = []
        topics += input
        for topic in input:
            syns = most_similar(topic)
            topics += syns
        wc_matrix = np.zeros((len(topics), len(debate_data.index)))
        score_matrix = np.zeros((len(debate_data.index,)))
        for data_idx in range(len(debate_data.index)):
            speech = debate_data['speech'][data_idx]
            column = wc_matrix[:,data_idx]
            it = np.nditer(column, flags=['f_index'], op_flags=['readwrite'])
            while not it.finished:
                idx = it.index
                it[0] = speech.count(topics[idx])
                it.iternext()
            score_matrix[data_idx] = np.sum(column)
        top_indices = (-score_matrix).argsort()[:n]
        for index in np.nditer(top_indices):
            trans_info = debate_data.loc[index]
            debate_name = trans_info['debate_name']
            if 'Transcript:' in debate_name: 
                debate_name.replace('Transcript:', '')
            obj = {"score": score_matrix[index], "debate_name": debate_name, "debate_date": trans_info['debate_date'], "speaker":trans_info['speaker'], "speech":trans_info['speech'], "link": trans_info["transcript_link"], "image":image_search(trans_info['speaker'])}
            final_data.append(obj)
        return final_data
    else:
        return