import streamlit as st
import numpy as np
from main import *
from streamlit_option_menu import option_menu
from itertools import compress
st.set_page_config(page_title="Universties Senegal",layout="wide")

def make_clickable(link):
    try:
        text = link.split('https://www.au-senegal.com/')[1]
    except:
        try:
            text = link.split('www.')[1]
        except:
            text = link.split('//')[1]
    return f'<a target="_blank" href="{link}">{text}</a>'



def main():
    st.sidebar.write("""# Hide:""")
    adresse = st.sidebar.checkbox('adresse')
    details = st.sidebar.checkbox('details')
    liens = st.sidebar.checkbox('liens')
    keywords = st.sidebar.checkbox('keywords')
    toggle_list = [adresse,details,liens,keywords]
    filt_list = list(compress(['adresse','details','liens','keywords'], toggle_list))
    st.write("""
            # Orientation SN

            ## Application for universities in Senegal with automatic keyword selection/indexing, using ***Python*** and ***Pandas Library***
            project files : https://github.com/abd2re/abd2re-university-sn-dataframe""")



    st.write("""Data cleansing done with jupyter and excel (pandas excel module)""")

    st.write("""University list from: https://infoetudes.com/liste-adresses-et-contacts-des-universites-ecoles-de-formations-et-instituts-du-senegal/""")

    st.write("""The keyword selection has been done by the code algorithm""")

    st.write("""# Filterable dataframe""")

    st.write("""***keywords auto-selected by frequency***""")
    arr = ''
    for i in keyword_dict:
        arr = arr + ' ' + i + ','
    st.write('['+arr[1:-1]+']')

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
    unis_filt.drop(['keywords_raw']+filt_list,axis=1,inplace=True)
    if toggle_list[2] == False:
        unis_filt['liens'] = unis_filt['liens'].apply(make_clickable)
    unis_filt = unis_filt.to_html(escape=False)

    st.write(unis_filt, unsafe_allow_html=True)

    st.write("""# Full dataframe""")
    st.dataframe(unis)
    st.write("""### Total: {}""".format(len(unis)))

def user():
    st.write("""# User customization""")
    options = st.multiselect('Choisi tes sujets:',list(keyword_dict.keys()))
    kws = options
    itera = 0
    unis_overall = []

    if len(kws) > 0:
        st.sidebar.write("""# Hide:""")
        adresse = st.sidebar.checkbox('adresse')
        details = st.sidebar.checkbox('details')
        liens = st.sidebar.checkbox('liens')
        toggle_list = [adresse,details,liens]
        filt_list = list(compress(['adresse','details','liens'], toggle_list))
        for elem in kws:
            line = 0
            unis_perso = unis.copy()
            for i in unis_perso['keywords']:
                for word in i:
                    if word == kws[itera]:
                        break
                else:
                    unis_perso.drop(line,axis=0,inplace=True)

                line += 1
            itera+=1
            unis_overall.append(unis_perso)
        unis_merged = pd.concat(unis_overall)
        unis_merged.drop_duplicates(subset='nom',inplace=True)

        points = np.zeros(len(unis_merged))
        freq_values = []

        for elem in kws:
            count = 0
            temp_values = []
            for i in unis_merged['keywords']:
                if elem in i:
                    points[count] += 1
                    temp_values.append(elem)
                else:
                    temp_values.append('')
                count +=1
            freq_values.append(temp_values)

        unis_merged.insert(3,'frequence',points)
        temp_freq_values = pd.DataFrame(freq_values).transpose().dropna().values.tolist()
        temp_freq_values = [' '.join(i).split() for i in temp_freq_values]
        unis_merged.insert(4,'selection',temp_freq_values)
        unis_merged.sort_values(by='frequence', ascending=False,inplace=True)
        unis_merged.drop(['keywords','keywords_raw']+filt_list,axis=1,inplace=True)
        if toggle_list[2] == False:
            unis_merged['liens'] = unis_merged['liens'].apply(make_clickable)
        unis_merged['frequence'] = unis_merged['frequence'].apply(lambda x: str(int(x))+'/'+str(len(kws)))
        unis_merged.set_index(np.arange(1,len(unis_merged)+1),inplace=True)
        unis_merged = unis_merged.to_html(escape=False)
        st.write(unis_merged, unsafe_allow_html=True)




selected = option_menu(
    menu_title=None,
    options=["Home", 'User'],
    icons=['house', 'cloud-upload'],
    orientation='horizontal'
    )


if selected == "Home":
    main()
if selected == "User":
    user()

