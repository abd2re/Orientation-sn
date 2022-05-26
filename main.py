import pandas as pd
import requests
from itertools import chain
from googlesearch import search
import os
import simplemma as splm
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


#try:
#    unis = pd.read_excel('unis_output_cor.xlsx','Sheet1')
#    url_link = 'https://infoetudes.com/liste-adresses-et-contacts-des-universites-ecoles-de-formations-et-instituts-du-senegal/'
#    r = requests.get(url_link,headers ={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
#    unis = pd.read_html(r.text)[0]
#    unis = unis.transpose()
#    unis.drop(0,axis=1,inplace=True)
#    unis.set_index(1,inplace=True)
#    unis = unis.transpose()
#    unis.reset_index(inplace=True)
#    unis.drop('index',axis=1,inplace=True)
#    unis.columns = ['nom', 'adresse', 'details[1]', 'details']
#    unis.dropna(thresh=3,inplace=True)
#    unis.drop('details[1]',axis=1,inplace=True)
#    unis.to_excel('unis_output.xlsx')
#except:
#    pass
unis = pd.read_excel('unis.xlsx','Sheet1')

unis.drop('Unnamed: 0',axis=1,inplace=True)
unis["nom"] = unis["nom"]
unis["adresse"] = unis["adresse"]
unis["details"] = unis["details"]
unis.fillna('',inplace=True)
keyword_list = []
for ndet in unis['details'].str.lower():
    ndet = ndet.replace(",","")
    ndet = ndet.replace(".","")
    ndet = ndet.replace("…","")
    ndet = ndet.replace("’", " ")
    ndet = ndet.replace("/", " ")
    for i in set(ndet.split()):
        if len(i) > 2:
            keyword_list.append(i)
new_keyword_list=[]
for i in keyword_list:
    if i[-1] == 's': i = i[:-1]
    if len(i) > 2:
        new_keyword_list.append(i)


langdata = splm.load_data('fr')
stop_words = set(stopwords.words('french'))

unvect = []
for i in unis['details']:
    word_tokens = word_tokenize(i)
    filtered_sentence = []
    for w in word_tokens:
        if w not in stop_words and len(w)>1:
            filtered_sentence.append(splm.lemmatize(w, langdata))

    sent = ' '.join(filtered_sentence)
    unvect.append(sent)

unis['unvectored'] = unvect
unis['unvectored'].mask(unis['unvectored'] == '',inplace=True)

unique_words = list(chain(*[unvect[i].split(" ") for i in range(len(unvect))]))

#print(unique_words)

keyword_series = pd.Series(unique_words)
keyword_series.value_counts().to_csv('keywordlist')
keyword_series = pd.read_csv('keywordlist')

keyword_series = keyword_series[keyword_series['0']>1]
print(keyword_series['Unnamed: 0'])
#for i in keyword_series['0']:
#    print(i)

#print(keyword_series)
#unis.drop(unis.iloc[:, 3:11], inplace = True, axis = 1)
keywords = []

print(unis['unvectored'])

for i in unvect:
    temp_key = []
    for word in i.split():
        if word in keyword_series.iloc[:,0].values:
            temp_key.append(word)
    keywords.append(list(set(temp_key)))

unis['keywords'] = keywords
links = []

if os.path.exists('unis_links') == False:
    for i in unis['nom']:
        query = i + ' senegal'
        for j in search(query, tld="sn", stop=1):
            links.append(j)
    unis['liens'] = links
    unis['liens'].to_csv('unis_links')

unis['liens'] = pd.read_csv('unis_links')['liens']

keyword_dict = dict(zip(keyword_series['Unnamed: 0'],keyword_series['0']))

#print(keyword_series)





