
import streamlit as st
import awesome_streamlit as ast
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import altair as alt
import time
import streamlit.components.v1 as components

from numpy import cov
from textblob import TextBlob
from scipy.stats import pearsonr

from PIL import Image


#....................................................Logic..........................................................

#Sentiment Analysis Polarity and Subjectivity

#Global Variables
Review_df = pd.DataFrame()
Sentiment_filter = pd.DataFrame()
Sentiment_desc = pd.DataFrame()
positive_count = pd.DataFrame()
negative_count = pd.DataFrame()
neutral_count = pd.DataFrame()

#Fetch and Create Review DataFrame
#@st.cache
def Pol_Sub(csv_file):
    
    global Review_df, Sentiment_filter, Sentiment_desc, positive_count, negative_count, neutral_count
    
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

    #Positive count
    positive_count = Sentiments_df.loc[Sentiments_df['Polarity'] >0] 

    #Negative count
    negative_count = Sentiments_df.loc[Sentiments_df['Polarity'] <0]

    #Neutral count
    neutral_count = Sentiments_df.loc[Sentiments_df['Polarity'] ==0]

    Sentiment_desc = pd.DataFrame(Sentiment_filter.describe())
    return 

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
    hist_data = [Sentiment_filter.Polarity.values, Sentiment_filter.Subjectivity.values]
    group_labels = ['Polarity','Subjectivity']
    colors = ['#333F44', '#37AA9C']
    fig = ff.create_distplot(hist_data, group_labels, show_hist=False, colors=colors)
    fig.update_layout(
        height= 700,
        width=1100
    )
    return st.plotly_chart(fig)
    

#..............................................................UI........................................................
def write():
    uploaded_file = st.sidebar.file_uploader("Choose a csv file for analysis", type='csv')
    components.html(f"""
             <link href="https://unpkg.com/tailwindcss@^1.0/dist/tailwind.min.css" rel="stylesheet">
                <div class="flex">
                    <div class="flex-auto rounded-md shadow-lg overflow-hidden text-white font-bold 
                    rounded-md text-xl bg-blue-500 text-center px-4 py-4 m-2">
                    Sentiment Analysis
                    </div>
                </div>
    """,height=90)
     
    
    if uploaded_file is not None:
        Pol_Sub(uploaded_file)

        positive_c= positive_count.shape
        negative_c= negative_count.shape
        neutral_c=  neutral_count.shape

        components.html(f"""
             <link href="https://unpkg.com/tailwindcss@^1.0/dist/tailwind.min.css" rel="stylesheet">
                
                <div class="flex justify-center  gap-x-2">
                    
                    <div class="max-w-sm overflow-hidden rounded-md shadow-lg">
                        <div class="text-md px-8 pt-4">Positive Statements</div>
                        <div class="text-center font-bold text-2xl pb-2 text-blue-500">
                            <span>{positive_c[0]}</span>
                        </div>
                    </div>

                    <div class="max-w-sm overflow-hidden rounded-md shadow-lg">
                        <div class="text-md px-8 pt-4">Negative Statements</div>
                        <div class="text-center font-bold text-2xl pb-2 text-red-500">
                            <span>{negative_c[0]}</span>
                        </div>
                    </div>

                    <div class="max-w-sm overflow-hidden rounded-md shadow-lg">
                        <div class="text-md px-8 pt-4">Neutral Statements</div>
                        <div class="text-center font-bold text-2xl pb-2 text-gray-500">
                            <span>{neutral_c[0]}</span>
                        </div>
                    </div>
                </div>""",height=100)

        mean = Sentiment_desc.loc['mean'].tolist()
        std = Sentiment_desc.loc['std'].tolist()
        mini = Sentiment_desc.loc['min'].tolist()
        maxi = Sentiment_desc.loc['max'].tolist() 

        components.html(f"""
             <link href="https://unpkg.com/tailwindcss@^1.0/dist/tailwind.min.css" rel="stylesheet">
                
                <div class="flex justify-center">
                    
                    <div class="rounded-lg shadow-lg overflow-hidden rounded-md bg-blue-500 px-4 py-4 ">
                        
                        <span class="text-white text-xl font-bold ">DataSet Overview</span>
                        
                        <div class="pt-4 text-white text-lg">
                            <span>Polarity<span>
                        <div>
                        
                        <div class="flex flex-wrap pt-4 gap-x-2 gap-y-2">    
                            <div class="bg-white rounded-md text-center shadow-lg">
                                <div class="text-sm px-10 text-blue-500 pt-2">Mean</div>
                                <div class="text-center font-bold text-md pb-2 text-blue-500">
                                    <span>{"{:.3f}".format(mean[0])}</span>
                                </div>
                            </div>    

                            <div class="bg-white rounded-md text-center shadow-lg">
                                <div class="text-sm px-10 text-blue-500 pt-2">STD</div>
                                <div class="text-center font-bold text-md pb-2 text-blue-500">
                                    <span>{"{:.3f}".format(std[0])}</span>
                                </div>
                            </div>    

                            <div class="bg-white rounded-md text-center shadow-lg">
                                <div class="text-sm px-10 text-blue-500 pt-2">Min</div>
                                <div class="text-center font-bold text-md pb-2 text-blue-500">
                                    <span>{"{:.2f}".format(mini[0])}</span>
                                </div>
                            </div>    

                            <div class="bg-white rounded-md text-center shadow-lg">
                                <div class="text-sm px-10 text-blue-500 pt-2">Max</div>
                                <div class="text-center font-bold text-md pb-2 text-blue-500">
                                    <span>{"{:.2f}".format(maxi[0])}</span>
                                </div>
                            </div>       
                        </div>

                        <div class="pt-4 text-white text-lg">
                            <span>Subjectivity<span>
                        <div>
                        
                        <div class="flex flex-wrap pt-4 gap-x-2 gap-y-2">    
                            <div class="bg-white rounded-md text-center shadow-lg">
                                <div class="text-sm px-10 text-blue-500 pt-2">Mean</div>
                                <div class="text-center font-bold text-md pb-2 text-blue-500">
                                    <span>{"{:.3f}".format(mean[1])}</span>
                                </div>
                            </div>    

                            <div class="bg-white rounded-md text-center shadow-lg">
                                <div class="text-sm px-10 text-blue-500 pt-2">STD</div>
                                <div class="text-center font-bold text-md pb-2 text-blue-500">
                                    <span>{"{:.3f}".format(std[1])}</span>
                                </div>
                            </div>    

                            <div class="bg-white rounded-md text-center shadow-lg">
                                <div class="text-sm px-10 text-blue-500 pt-2">Min</div>
                                <div class="text-center font-bold text-md pb-2 text-blue-500">
                                    <span>{"{:.2f}".format(mini[1])}</span>
                                </div>
                            </div>    

                            <div class="bg-white rounded-md text-center shadow-lg">
                                <div class="text-sm px-10 text-blue-500 pt-2">Max</div>
                                <div class="text-center font-bold text-md pb-2 text-blue-500">
                                    <span>{"{:.2f}".format(maxi[1])}</span>
                                </div>
                            </div>       
                        </div>
                    </div>   
                </div>""",height=310)

        Pol_dist()
        
        #Raw DataSet
        if st.sidebar.checkbox("Show Dataset"):
            st.subheader('Dataset')
            st.write(Review_df)    

    else:
        st.subheader('Upload data file!!')

if __name__=="__main__":
    write()

