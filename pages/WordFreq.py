import streamlit as st
import awesome_streamlit as ast
import streamlit.components.v1 as components

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
def Word_Freq():
    count = 10
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
    fig = px.bar(result_count, x='Word', y='Frequency',
             hover_data=['Word', 'Frequency'], color='Frequency',
              height=700, width=1100)
    fig.update_layout(
        paper_bgcolor='rgb(40,44,53)',
        plot_bgcolor='rgb(40,44,53)',
        font_color="white"  
    )
    
    return st.plotly_chart(fig)

#Word Cloud
def Word_Cloud():
    stopwords = nltk.corpus.stopwords.words('english')
    RE_Stopword = r'\b(?:{})\b'.format('|'.join(stopwords))
    word = (Review_df['Review'].replace([r'\!',r'\@',r'\#',r'\$',r'\%',r'\-',r'\&',r'\*',r'\(',r'\'',r'\.',r'\,',r'\_',r'\>','car',
                                     RE_Stopword], 
                                    ['','','','','','','','','','','','','','','',''], 
                                    regex=True).str.cat(sep=' ').split())
    wordcloud = WordCloud(max_font_size=150, width=1920, height=1080, colormap='brg',
                      background_color='#282C35').generate(' '.join(word))
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.tight_layout(pad = 0) 
    return st.pyplot()


#..........................................User InterFace....................................................#
def write():
    
    uploaded_file = st.sidebar.file_uploader("Choose a csv file for analysis", type='csv', key='sent')

    components.html(f"""
             <link href="https://unpkg.com/tailwindcss@^1.0/dist/tailwind.min.css" rel="stylesheet">
                <div class="flex">
                    <div class="flex-auto rounded-md shadow-lg overflow-hidden text-gray-400 font-bold 
                    rounded-md text-xl border-2 border-blue-500 text-center px-4 py-4 m-2">
                    Keyword Analysis
                    </div>
                </div>
    """,height=90)
    
    if uploaded_file is not None:
        
        Pol_Sub(uploaded_file)
        Word_Freq()

        words = result_count['Word'].values.tolist()
        frequency = result_count['Frequency'].values.tolist()

        components.html(f"""
             <link href="https://unpkg.com/tailwindcss@^1.0/dist/tailwind.min.css" rel="stylesheet">
                
                <div class="flex justify-center">
                    <div class="flex rounded-md shadow-xl px-4 py-4 m-2">
                        <span class="text-blue-500 text-center font-bold text-lg">Top 10 words with maximum frequency<span>

                        <div class="flex flex-wrap justify-center pt-4 gap-x-2 gap-y-2">
                            
                            <div class="rounded-md text-center shadow-lg">
                                <div class="text-sm px-10 text-indigo-700 pt-2">{words[0]}</div>
                                <div class="text-center font-bold text-md pb-2 text-blue-500">
                                    <span>{frequency[0]}</span>
                                </div>
                            </div>     

                            <div class="rounded-md text-center shadow-lg">
                                <div class="text-sm px-10 text-indigo-700 pt-2">{words[1]}</div>
                                <div class="text-center font-bold text-md pb-2 text-blue-500">
                                    <span>{frequency[1]}</span>
                                </div>
                            </div>     

                            <div class="rounded-md text-center shadow-lg">
                                <div class="text-sm px-10 text-indigo-700 pt-2">{words[2]}</div>
                                <div class="text-center font-bold text-md pb-2 text-blue-500">
                                    <span>{frequency[2]}</span>
                                </div>
                            </div>     

                            <div class="rounded-md text-center shadow-lg">
                                <div class="text-sm px-10 text-indigo-700 pt-2">{words[3]}</div>
                                <div class="text-center font-bold text-md pb-2 text-blue-500">
                                    <span>{frequency[3]}</span>
                                </div>
                            </div>     

                            <div class="rounded-md text-center shadow-lg">
                                <div class="text-sm px-10 text-indigo-700 pt-2">{words[4]}</div>
                                <div class="text-center font-bold text-lg pb-2 text-blue-500">
                                    <span>{frequency[4]}</span>
                                </div>
                            </div>     
                        </div>

                        <div class="flex flex-wrap justify-center pt-4 gap-x-2 gap-y-2">
                            <div class="rounded-md text-center shadow-lg">
                                <div class="text-sm px-10 text-indigo-700 pt-2">{words[5]}</div>
                                <div class="text-center font-bold text-md pb-2 text-blue-500">
                                    <span>{frequency[5]}</span>
                                </div>
                            </div>     

                            <div class="rounded-md text-center shadow-lg">
                                <div class="text-sm px-10 text-indigo-700 pt-2">{words[6]}</div>
                                <div class="text-center font-bold text-md pb-2 text-blue-500">
                                    <span>{frequency[6]}</span>
                                </div>
                            </div>     

                            <div class="rounded-md text-center shadow-lg">
                                <div class="text-sm px-10 text-indigo-700 pt-2">{words[7]}</div>
                                <div class="text-center font-bold text-md pb-2 text-blue-500">
                                    <span>{frequency[7]}</span>
                                </div>
                            </div>     

                            <div class="rounded-md text-center shadow-lg">
                                <div class="text-sm px-10 text-indigo-700 pt-2">{words[8]}</div>
                                <div class="text-center font-bold text-md pb-2 text-blue-500">
                                    <span>{frequency[8]}</span>
                                </div>
                            </div>     

                            <div class="rounded-md text-center shadow-lg">
                                <div class="text-sm px-10 pt-2 text-indigo-700">{words[9]}</div>
                                <div class="text-center font-bold text-md pb-2 text-blue-500">
                                    <span>{frequency[9]}</span>
                                </div>
                            </div>     
                        </div>
                        </div>
                    </div>
                </div>         
                """,height=250)
        
        Bar_chart()

        components.html(f"""
             <link href="https://unpkg.com/tailwindcss@^1.0/dist/tailwind.min.css" rel="stylesheet">
                <div class="flex">
                    <div class="flex-auto rounded-md shadow-lg overflow-hidden text-gray-400 font-bold 
                    rounded-md text-xl border-2 border-blue-500 text-center px-4 py-4 m-2">
                    Keyword Cloud
                    </div>
                </div>
    """,height=90)
        
        Word_Cloud()    

    else:
        st.subheader('Upload data file!!')

if __name__=="__main__":
    write()

