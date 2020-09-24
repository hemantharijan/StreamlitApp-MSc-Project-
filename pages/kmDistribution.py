import streamlit as st
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import plotly.graph_objects as go
import streamlit.components.v1 as components
import seaborn as sns
sns.set()

#..................................................Logic....................................................#
df = pd.DataFrame()

# Seperate data by specified range
def range(data):
    global df
    df = pd.read_csv(data, engine='python')
    return

#Bar plot
def countplot(start, end):
    df_km_count = pd.DataFrame(df['Km_Driven'].value_counts())
    df_km_count.reset_index(inplace=True)
    df_km_count.columns = ['Km_Driven','count']
    df_km_count.sort_values(by=['Km_Driven'], inplace=True)
    Range = df_km_count.iloc[start:end]
    fig = px.bar(Range, x='Km_Driven', y='count',  
                hover_data=['Km_Driven','count'], color='count', height=620, width=1100
    )
    fig.update_layout(  
        paper_bgcolor='rgb(40,44,53)',
        plot_bgcolor='rgb(40,44,53)',
        font_color="white"
    )
    return st.plotly_chart(fig)

#..................................................User-Interface....................................................#

def write():

    components.html(f"""
             <link href="https://unpkg.com/tailwindcss@^1.0/dist/tailwind.min.css" rel="stylesheet">
                <div class="flex">
                    <div class="flex-auto rounded-md shadow-lg overflow-hidden text-gray-400 font-bold 
                    rounded-md text-xl border-2 border-blue-500 text-center px-4 py-4 m-2">
                    Kilometer Analysis
                    </div>
                </div>
    """,height=90)

    fileupload = st.sidebar.file_uploader('upload car data file', type='csv')

    if fileupload is not None:

        sub_menu = ['5k to 30k','40k to 70k','80k to 150k']
        choice = st.sidebar.radio("",sub_menu)
        range(fileupload)

        if choice == '5k to 30k':
            countplot(0,4)
        elif choice == '40k to 70k':
            countplot(4,8)
        elif choice == '80k to 150k':
            countplot(8,13)
            
    else:
        st.subheader('Upload data file!!')       

if __name__=="__main__":
    write()

