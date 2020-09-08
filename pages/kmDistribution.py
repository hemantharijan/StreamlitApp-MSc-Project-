import streamlit as st
import awesome_streamlit as ast
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

km_df = pd.DataFrame()
df = pd.DataFrame()
def range(data, first, last):
    global km_df, df
    df = pd.read_csv(data, engine='python')
    km_df = df.query('Km_Driven >='+str(first)+'and Km_Driven <='+str(last))
    #st.write(km_df)
    return

def countplot():
    f = plt.figure(figsize=(10,4))
    sns.countplot(x=km_df['Km_Driven'], data=km_df)
    return st.pyplot()

def scatterPlot():
    fig = go.Figure(data=go.Scatter(
    x= df['Km_Driven'],
    y= df['Price_inEURO'],
    mode='markers',
    #height=700,
    marker=dict(
        size=8,
        color= df['Price_inEURO'], 
        colorscale='Viridis',
        showscale=True
    )))
    return st.plotly_chart(fig)



def write():

    components.html(f"""
             <link href="https://unpkg.com/tailwindcss@^1.0/dist/tailwind.min.css" rel="stylesheet">
                <div class="flex">
                    <div class="flex-auto rounded-md shadow-lg overflow-hidden text-white font-bold rounded-md text-xl bg-blue-500 text-center px-4 py-4 m-2">
                    Kilometer Distribution
                    </div>
                </div>
    """,height=75)

    fileupload = st.sidebar.file_uploader('upload car data file', type='csv')

    if fileupload is not None:

        sub_menu = ['5k to 30k','40k to 70k','80k to 150k','Price over Kilometer']

        choice = st.sidebar.radio("",sub_menu)

        if choice == '5k to 30k':
            range(fileupload,5000,30000)
            countplot()

        elif choice == '40k to 70k':
            range(fileupload,40000,70000)
            countplot()
        
        elif choice == '80k to 150k':
            range(fileupload,80000,150000)
            countplot()

        elif choice == 'Price over Kilometer':
            scatterPlot()
            


if __name__=="__main__":
    write()

