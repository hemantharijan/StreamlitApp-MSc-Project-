import nltk
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.figure_factory as ff

from numpy import cov
from textblob import TextBlob
from collections import Counter
from scipy.stats import pearsonr
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator


st.set_option('deprecation.showfileUploaderEncoding', False)


#User Interface setting
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
#local_css("style.css")

hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 



#Sentiment Analysis Polarity and Subjectivity
#Fetch and Create Review DataFrame
Review_df = pd.DataFrame()
Sentiment_filter = pd.DataFrame()
#@st.cache
def Pol_Sub(csv_file):
    global Review_df, Sentiment_filter
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


# box plot
def boxplot():
    box_fig = px.box(Sentiment_filter)
    box_fig.update_layout(
        xaxis_title="Sentiments in terms of polarity and Subjectivity",
        yaxis_title="Range",)
    return st.plotly_chart(box_fig)


# Scatter plot
def scatterplot():
    scatter_fig = px.scatter(Sentiment_filter, x="Polarity", y="Subjectivity")
    return st.plotly_chart(scatter_fig)


#Covariance and Correlation
#Covariance
def Cov():
    polarity = Sentiment_filter['Polarity']
    subjectivity = Sentiment_filter['Subjectivity']
    #Finding Covariance
    covariance = cov(polarity, subjectivity)
    #print('Covariance Result')
    #print(covariance)
    #Finding Correlation
    #print('Correlation:',corr)
    return covariance
#correlation
def Corr():
    polarity = Sentiment_filter['Polarity']
    subjectivity = Sentiment_filter['Subjectivity']
    corr,_ = pearsonr(polarity, subjectivity)
    return corr


#Polarity Distribution
def Pol_dist():
    hist_data = [Sentiment_filter.Polarity.values.tolist()]
    hist_fig = ff.create_distplot(hist_data, group_labels=['Polarity'], bin_size=.05)
    return st.plotly_chart(hist_fig)


#Frequent Word
result_count = pd.DataFrame()
def Word_Freq():
    global result_count
    stopwords = nltk.corpus.stopwords.words('english')
    RE_Stopword = r'\b(?:{})\b'.format('|'.join(stopwords))
    word = (Review_df['Review'].replace([r'\!',r'\@',r'\#',r'\$',r'\%',r'\-',r'\&',r'\*',r'\(',r'\'',r'\.',r'\,','r\_',r'\>',
                                     RE_Stopword], 
                                    ['','','','','','','','','','','','','','',''], 
                                    regex=True).str.cat(sep=' ').split())
    result_count = pd.DataFrame(Counter(word).most_common(10),columns=['Word','Frequency'])
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
    word = (Review_df['Review'].replace([r'\!',r'\@',r'\#',r'\$',r'\%',r'\-',r'\&',r'\*',r'\(',r'\'',r'\.',r'\,','r\_',r'\>',
                                     RE_Stopword], 
                                    ['','','','','','','','','','','','','','',''], 
                                    regex=True).str.cat(sep=' ').split())
    wordcloud = WordCloud(min_font_size=30, width=700, height=700, colormap='brg',
                      background_color='white').generate(' '.join(word))
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.tight_layout(pad = 0) 
    return st.pyplot()


#Dashboard
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
        
        #Raw DataSet
        if st.sidebar.checkbox("Show Raw Data"):
            st.write(Review_df)    
        
        #BoxPlot
        st.subheader('Box Plot')
        st.write(boxplot())

        #ScatterPlot
        st.subheader('Scatter Plot')
        st.write(scatterplot())

        #Covariance
        st.subheader('Covariance')
        st.write(Cov())

        #Correlation
        st.subheader('Correlation')
        st.text(Corr())

        #Polarity Distribution
        st.subheader('Polarity distribution')
        st.write(Pol_dist())

        #Frequent Words
        st.subheader('Most Frequent words in DataSet')
        st.write(Word_Freq())

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
        st.write('No data')
       
elif choice == 'Used Cars Data':
    file_path = st.file_uploader('upload file', type='csv')
    if file_path is not None:
        data = pd.read_csv(file_path)
        st.dataframe(data)





