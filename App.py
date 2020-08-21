import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import nltk
import plotly.figure_factory as ff
from textblob import TextBlob
from numpy import cov
from scipy.stats import pearsonr
from collections import Counter
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator


st.set_option('deprecation.showfileUploaderEncoding', False)
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
#local_css("style.css")

#Sentiment Analysis
#Fetch and Create Review DataFrame
Review_df = pd.DataFrame()
#@st.cache
def Pol_Sub(csv_file):
    global Review_df
    df = pd.read_csv(csv_file, encoding='utf-8', engine='python')
    Review_df = pd.DataFrame(df['Review'].str.lower())
    Review_df['Review'].replace('\d+', '', regex=True, inplace=True)

    #Analysing sentiments in terms of polarity and subjectivity
    Polarity =[]
    Subjectivity = []

    #Iterating every row in the column
    for row in Review_df['Review']:
                    
        text = str(row)
        blob = TextBlob(text)
                    
        Sentiment = blob.sentiment
                    
        polarity = Sentiment.polarity          #Calculating polarity of each review
        subjectivity = Sentiment.subjectivity  #Calculating subjectivity of each review
                    
        Polarity.append(polarity)              #populating polarity list
        Subjectivity.append(subjectivity)      #populating subjectivity list
                    
        #Creating dictionary of list for Creating DataFrame
        dicts = {'Polarity':Polarity,'Subjectivity':Subjectivity}
        Sentiments_df = pd.DataFrame(dicts)

        #Filtering Sentiments_df by excluding neutral reviews for accurate values
        Sentiment_filter = Sentiments_df.loc[(Sentiments_df.loc[:,Sentiments_df.dtypes != object] !=0).any(1)] 
        Sentiment_desc = pd.DataFrame(Sentiment_filter.describe())
        return Sentiment_desc

#UI
st.title('Used Car Price Analytics and Prediction')

#SideBar Menu
menu = ['Select','Sentiment Analysis','Used Cars Data']

choice = st.sidebar.selectbox("Menu",menu)

#Sentiment Analysis
if choice == 'Sentiment Analysis':
    
    st.header('Sentiment Analysis on user reviews')
    
    #upload csv file
    st.write(" Upload csv file")
    uploaded_file = st.file_uploader("Choose a csv file", type='csv')
    
    if uploaded_file is not None:
        st.write(Pol_Sub(uploaded_file))
        if st.checkbox("Show Raw Data"):
            st.write(Review_df)

        
    else:
        st.write('No data')
       

elif choice == 'Used Cars Data':
    file_path = st.file_uploader('upload file', type='csv')
    if file_path is not None:
        data = pd.read_csv(file_path)
        st.dataframe(data)





