import streamlit as st
import numpy as np
from main import *

st.set_page_config(layout="wide")

#st.write("""
         # Data Science Personal Project

         ## Application for universities in Senegal with automatic keyword selection/indexing, using ***Python*** and ***Pandas Library***
         #project files : https://github.com/abd2re/abd2re-university-sn-dataframe""")



st.write("""Liste des universites au Senegal""")

#st.write("""University list from: https://infoetudes.com/liste-adresses-et-contacts-des-universites-ecoles-de-formations-et-instituts-du-senegal/""")

#st.write("""The keyword selection has been done by the code algorithm""")


#st.write("""# Full dataframe""")
st.dataframe(unis)
st.write("""### Total: {}""".format(len(unis)))

#st.write("""# Filterable dataframe""")

#st.write("""***keywords auto-selected by frequency***""")
arr = ''
#for i in keyword_dict:
#    arr = arr + ' ' + i + ','
#st.write('['+arr[1:-1]+']')

val = st.selectbox('Choose',keyword_dict.items())
kw = val[0]
unis_filt = unis.copy()
line = 0

for i in unis_filt['keywords']:
    for word in i:
        if word == kw:
            break
    else:
        unis_filt.drop(line,axis=0,inplace=True)

    line += 1

try:
    unis_filt = unis_filt.set_index(np.arange(1,val[1]+1))
except:
    unis_filt = unis_filt.set_index(np.arange(1,val[1]))

st.write("""### {} ({})""".format(kw,val[1]))
st.table(unis_filt.drop(['keywords_raw','keywords'],axis=1))


