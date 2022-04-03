#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import requests

unis = pd.read_excel('unis_output_cor.xlsx','Sheet1')
url_link = 'https://infoetudes.com/liste-adresses-et-contacts-des-universites-ecoles-de-formations-et-instituts-du-senegal/'
r = requests.get(url_link,headers ={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
unis = pd.read_html(r.text)[0]
unis = unis.transpose()
unis.drop(0,axis=1,inplace=True)
unis.set_index(1,inplace=True)
unis = unis.transpose()
unis.reset_index(inplace=True)
unis.drop('index',axis=1,inplace=True)
unis.columns = ['nom', 'adresse', 'details[1]', 'details']
unis.dropna(thresh=3,inplace=True)
unis.drop('details[1]',axis=1,inplace=True)
unis.to_excel('unis_output.xlsx')
unis = pd.read_excel('unis_output_cor.xlsx','Sheet1')
unis.drop('Unnamed: 0',axis=1,inplace=True)
unis["nom"] = unis["nom"].str.lower()
unis["adresse"] = unis["adresse"].str.lower()
unis["details"] = unis["details"].str.lower()
unis.fillna('',inplace=True)
keyword_list = []
for ndet in unis['details']:
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
keyword_series = pd.Series(new_keyword_list)
keyword_series.value_counts().to_csv('keywordlist')





keyword_series = pd.read_csv('keywordlist_cor.txt')
details_mod = []
for i in unis['details']:
    phrase = ''
    i = i.replace(",","")
    i = i.replace(".","")
    i = i.replace("…","")
    i = i.replace("’", " ")
    i = i.replace("/", " ")
    for word in i.split():
        if word[-1] == 's':
            word = word[:-1]
        phrase = phrase +''.join(word) + ' '
    details_mod.append(phrase)
unis['keywords_raw'] = details_mod
unis.drop(unis.iloc[:, 3:11], inplace = True, axis = 1)
keywords = []
for i in unis['keywords_raw']:
    temp_key = []
    for word in i.split():
        if word in keyword_series.iloc[:,0].values:
            temp_key.append(word)
    keywords.append(list(set(temp_key)))

unis['keywords'] = keywords
unis.drop([89,90,91,92,93,94],axis=0,inplace=True)

keyword_dict = dict(zip(keyword_series['keyword'],keyword_series['count']))






