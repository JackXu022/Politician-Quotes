import pandas as pd
import re
import numpy as np
import math
from app.irsystem.models.BingImageSearchv7 import image_search

def tokenize(str):
    str = str.lower()
    return re.findall("[a-z]+", str)

docs = []
data = pd.read_csv('app/data/debate_transcripts_v5.csv')
for i in range(0, len(data['speech'])):
    docs.append(dict())
    docs[i]['speaker'] = data['speaker'][i]
    docs[i]['text'] = tokenize(data['speech'][i])

def build_inverted_index(msgs):
    result = dict()
    for i in range(0, len(msgs)):
        for word in msgs[i]['text']:
            if word in result:
                if i in result[word]:
                    result[word][i] += 1
                else:
                    result[word][i] = 1
            else:
                result[word] = dict()
                result[word][i] = 1
    tups = dict()
    for i in result:
        tups[i] = []
        for key in result[i]:
            tups[i].append((key, result[i][key]))
    return tups

inv_idx = build_inverted_index(docs)

def compute_idf(inv_idx, n_docs, min_df=5, max_df_ratio=0.9):
    result = dict()
    max_df = n_docs * max_df_ratio
    for i in inv_idx:
        if len(inv_idx[i]) >= min_df and len(inv_idx[i]) <= max_df:
            result[i] = math.log(n_docs / (1 + len(inv_idx[i])), 2)
        
    return result

idf = compute_idf(inv_idx, len(data['speech']))

def compute_doc_norms(index, idf, n_docs):
    norms = np.zeros(n_docs)
    for i in index:
        if i in idf:
            for j in range(0, len(index[i])):
                norms[index[i][j][0]] += (index[i][j][1] * idf[i])**2
    for i in range(0, len(norms)):
        norms[i] = norms[i]**.5
    return norms



inv_idx = {key: val for key, val in inv_idx.items()
           if key in idf}            

doc_norms = compute_doc_norms(inv_idx, idf, len(data['speech']))


def index_search(q, index, idf, doc_norms, tokenizer=tokenize):
    
    #q = tokenizer(query.lower())
    q_words = dict()
    for i in q:
        if i in q_words:
            q_words[i] += 1
        else:
            q_words[i] = 1
    q_norm = 0
    for i in q_words:
        if i in idf:
            q_norm += (q_words[i] * idf[i])**2
    q_norm = q_norm**.5
   
    scores = dict()
    for word in q:
        if word in idf:
            for doc in index[word]:
                if doc[0] in scores:
                    scores[doc[0]] += q_words[word] * idf[word] * doc[1] * idf[word]
                else:
                    scores[doc[0]] = q_words[word] * idf[word] * doc[1] * idf[word]
    result = []
    for i in scores:
        result.append((scores[i] / (q_norm * doc_norms[i]), i))
        
    results = sorted(result, reverse = True)
    
    
    return results

def sim_list(doc_id):        #produces 5 most similar docs to doc_id
    sim_list = index_search(docs[doc_id]['text'], inv_idx, idf, doc_norms)
    result = []
    for i in range(0, 5):
        result.append(sim_list[i][1])
    return result

def get_5_sim_cosine(str):
    q = tokenize(str.lower())
    final_data = []
    sim_list = index_search(q, inv_idx, idf, doc_norms)
    for i in range(0, 5):
        idx = sim_list[i][1]
        obj = {"score": sim_list[i][0], "debate_name": data['debate_name'][idx], "debate_date": data['debate_date'][idx], "speaker":data['speaker'][idx], "speech":data['speech'][idx], "link": data["transcript_link"][idx] }
        final_data.append(obj)
    return final_data

def get_top_n(query, n, politicians):
    #query: query string
    #n: number (int) of desired results
    #politicians: string
    
    check_pol = True
    if n:
        n=int(n)
    else:
        n=10

    if not politicians and not query:
        return

    if not query:
        return

    if not politicians:
        check_pol = False
    else:
        politicians = [p.strip() for p in politicians.split(",")]
        input_politicians = []
        for politician in politicians:
            item = politician.split()
            word = ""
            for name in item:
                word += name.capitalize() + " "
            input_politicians.append(word.strip())
        input_politicians = set(input_politicians)
        print(input_politicians)

    q = tokenize(query)

    sim_list = index_search(q, inv_idx, idf, doc_norms)
    count = 0
    i = 0
    final_data = []
    while count < n and i < len(sim_list):
        idx = sim_list[i][1]
        if(check_pol):
            if data['speaker'][idx] in input_politicians:
                obj = {"score": sim_list[i][0], "debate_name": data['debate_name'][idx], "debate_date": data['debate_date'][idx], "speaker":data['speaker'][idx], "speech":data['speech'][idx], "link": data["transcript_link"][idx], "image":image_search(data['speaker'][idx])}
                final_data.append(obj)
                count += 1
        else:
                obj = {"score": sim_list[i][0], "debate_name": data['debate_name'][idx], "debate_date": data['debate_date'][idx], "speaker":data['speaker'][idx], "speech":data['speech'][idx], "link": data["transcript_link"][idx], "image":image_search(data['speaker'][idx]) }
                final_data.append(obj)
                count += 1
        i += 1
    return final_data