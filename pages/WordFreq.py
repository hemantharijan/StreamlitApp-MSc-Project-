import streamlit as st
import awesome_streamlit as ast

import nltk
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.figure_factory as ff

from io import StringIO, BytesIO
from textblob import TextBlob
from collections import Counter
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator


#..........................................Back end logic....................................................#

Review_df = pd.DataFrame()

def Pol_Sub(csv_file):
    
    global Review_df

    df = pd.read_csv(csv_file, encoding='utf-8', engine='python')
    Review_df = pd.DataFrame(df['Review'].str.lower())
    Review_df['Review'].replace('\d+', '', regex=True, inplace=True)
    return

#Global Variable
result_count = pd.DataFrame()

#Frequent Word
def Word_Freq(count):
    count = int(count)
    global result_count
    stopwords = nltk.corpus.stopwords.words('english')
    RE_Stopword = r'\b(?:{})\b'.format('|'.join(stopwords))
    word = (Review_df['Review'].replace([r'\!',r'\@',r'\#',r'\$',r'\%',r'\-',r'\&',r'\*',
                                    r'\(',r'\'',r'\.',r'\,',r'\_',r'\>',r'\’',RE_Stopword], 
                                    ['','','','','','','','','','','','','','','',''], 
                                    regex=True).str.cat(sep=' ').split())
    count = pd.DataFrame(Counter(word).most_common(count+1),columns=['Word','Frequency'])
    count.drop(count.loc[count['Word']== 'car'].index, inplace=True)
    result_count = pd.DataFrame(count)
    return result_count


#Bar Chart
def Bar_chart():
    bar_fig = px.bar(result_count, x='Word', y='Frequency')
    return st.plotly_chart(bar_fig)


#Pie Chart
def Pie_chart():
    pie_fig = px.pie(result_count,values='Frequency',names='Word')
    return st.plotly_chart(pie_fig)


#Word Cloud
def Word_Cloud():
    stopwords = nltk.corpus.stopwords.words('english')
    RE_Stopword = r'\b(?:{})\b'.format('|'.join(stopwords))
    word = (Review_df['Review'].replace([r'\!',r'\@',r'\#',r'\$',r'\%',r'\-',r'\&',r'\*',r'\(',r'\'',r'\.',r'\,',r'\_',r'\>','car',
                                     RE_Stopword], 
                                    ['','','','','','','','','','','','','','','',''], 
                                    regex=True).str.cat(sep=' ').split())
    wordcloud = WordCloud(max_font_size=100, width=700, height=700, colormap='brg',
                      background_color='white').generate(' '.join(word))
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.tight_layout(pad = 0) 
    return st.pyplot()


#..........................................User InterFace....................................................#
def write():
    st.title("Word Frequency")
    
    uploaded_file = st.file_uploader("Choose a csv file for analysis", type='csv')
    if uploaded_file is not None:
        Pol_Sub(uploaded_file)
        
        #Frequent Words
        st.header("Word Frequency Analysis")
        count = st.sidebar.number_input("Word count number",min_value=10.00, step=1.00)

        #File Check
        # if uploaded_file is not None:
        st.subheader('Most Frequent words in DataSet')
        
        #Word count
        st.write(Word_Freq(count))

        #Bar Chart
        st.subheader('Bar Chart')
        st.write(Bar_chart())

        #Pie Chart
        st.subheader('Pie Chart')
        st.write(Pie_chart())

        #Word Cloud
        st.subheader('Word Cloud')
        st.write(Word_Cloud())

    else:
        st.subheader('Please upload a csv file')


if __name__=="__main__":
    write()

