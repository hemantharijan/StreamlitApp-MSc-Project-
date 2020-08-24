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


#..........................................Style Settings....................................................#

#CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
local_css("style.css")

#Hiding footer
hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 



#..........................................Back end logic....................................................#

#Sentiment Analysis Polarity and Subjectivity

#Global Variables
Review_df = pd.DataFrame()
Sentiment_filter = pd.DataFrame()
Sentiment_desc = pd.DataFrame()

#Fetch and Create Review DataFrame
#@st.cache
def Pol_Sub(csv_file):
    
    global Review_df, Sentiment_filter, Sentiment_desc
    
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
    return 


#Sentiment Analysis

#box plot
def boxplot():
    box_fig = px.box(Sentiment_filter)
    box_fig.update_layout(
        xaxis_title="Sentiments in terms of polarity and Subjectivity",
        yaxis_title="Range")
    return st.plotly_chart(box_fig)


#Scatter plot
def scatterplot():
    scatter_fig = px.scatter(Sentiment_filter, x="Polarity", y="Subjectivity")
    return st.plotly_chart(scatter_fig)


#Covariance and Correlation
#Covariance
def Cov():
    polarity = Sentiment_filter['Polarity']
    subjectivity = Sentiment_filter['Subjectivity']   
    covariance = cov(polarity, subjectivity)                 #Finding Covariance
    return covariance
#correlation
corr = 0.0
def Corr():
    global corr
    polarity = Sentiment_filter['Polarity']
    subjectivity = Sentiment_filter['Subjectivity']    
    corr,_ = pearsonr(polarity, subjectivity)              #Finding Correlation
    return corr


#Polarity Distribution
def Pol_dist():
    hist_data = [Sentiment_filter.Polarity.values.tolist()]
    hist_fig = ff.create_distplot(hist_data, group_labels=['Polarity'], bin_size=.05)
    return st.plotly_chart(hist_fig)


#Word Frequency Analysis

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
    result_count = pd.DataFrame(Counter(word).most_common(count),columns=['Word','Frequency'])
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
    wordcloud = WordCloud(max_font_size=100, width=700, height=700, colormap='brg',
                      background_color='white').generate(' '.join(word))
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.tight_layout(pad = 0) 
    return st.pyplot()


#..........................................User InterFace....................................................#

#Dashboard
st.title('Used Car Price Analytics and Prediction')

#upload csv file
uploaded_file = st.file_uploader("Choose a csv file", type='csv')
if uploaded_file is not None:
    Pol_Sub(uploaded_file)
    st.success('File is Uploaded')

#SideBar Menu
menu = ['Upload File','Sentiment Analysis','Word Frequency']
choice = st.sidebar.selectbox("Menu",menu)


#Sentiment Analysis
if choice == 'Sentiment Analysis':   
    
    #header
    st.header('Sentiment Analysis on user reviews')     
    
    #File Check
    if uploaded_file is not None:
        st.subheader("Polarity and Subjectivity")
        st.write(Sentiment_desc)
        
        #Raw DataSet
        if st.sidebar.checkbox("Show Dataset"):
            st.subheader('Dataset')
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

        if corr >= 0.0:
            st.success("From our above analysis the polarity increases as subjectivity increases and the correlation betweent them is positive, so the overall Feedback  is towards positive direction")
    else:
        st.subheader('Please upload a csv file!!')

#Word Frequency Analysis      
elif choice == 'Word Frequency':

    #Frequent Words
    st.header("Word Frequency Analysis")
    count = st.sidebar.number_input("Word count number",min_value=10.00, step=1.00)

    #File Check
    if uploaded_file is not None:
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




