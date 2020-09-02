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


df = pd.DataFrame()
def carData(data):
    global df
    df = pd.DataFrame(pd.read_csv(data,engine="python"))
    df= df.set_index('srno')
    return

df_brand = pd.DataFrame()
def brand(brandname):
    global df_brand
    df_brand= df.loc[df['Brand']==brandname]
    return 

def scatterPlot():
    fig = go.Figure(data=go.Scatter(
    x=df_brand['Year_Of_Registration'],
    y=df_brand['Price_inEURO'],
    mode='markers',
    marker=dict(
        size=16,
        color= df_brand['Price_inEURO'], 
        colorscale='Viridis',
        showscale=True
    )))
    return st.plotly_chart(fig)


def write():

    data = st.sidebar.file_uploader('upload car data file', type='csv')
    
    if data is not None:    
        
        carData(data)
        brandlist = df['Brand'].unique().tolist()
        brandname = st.selectbox('Select car brand',brandlist)
        brand(brandname)

        data_count = df_brand.shape
        ywmd = df_brand.loc[df_brand['Price_inEURO']==df_brand['Price_inEURO'].max()]
        ywmd = ywmd['Year_Of_Registration'].values.tolist()

        components.html(f"""
            <link href="https://unpkg.com/tailwindcss@^1.0/dist/tailwind.min.css" rel="stylesheet">

            <div class="flex">
    
                <div class="max-w-sm rounded-md overflow-hidden shadow-lg">
                    <div class="px-6 pt-2">
                        <div class="text-l"><span>Total Count</span></div>
                    </div>
                    <div class="px-6 font-bold text-xl pb-2"><span>{data_count[0]}</span></div>
                </div>
    
                <div class="max-w-sm rounded-md overflow-hidden shadow-lg">
                    <div class="px-6 pt-2">
                        <div class="text-l"><span>Max Price</span></div>
                    </div>
                    <div class="px-6 font-bold text-xl pb-2"><span>{df_brand['Price_inEURO'].max()} €</span></div>
                </div>
    
                <div class="max-w-sm rounded-md overflow-hidden shadow-lg">
                    <div class="px-6 pt-2">
                        <div class="text-l"><span>Min Price</span></div>
                    </div>
                    <div class="px-6 text-xl font-bold pb-2"><span>{df_brand['Price_inEURO'].min()} €</span></div>
                </div>

                <div class="max-w-sm rounded-md overflow-hidden shadow-lg">
                    <div class="px-6 pt-2">
                        <div class="text-l"><span>Year with max distribution</span></div>
                    </div>
                    <div class="px-6 pb-2 text-xl font-bold"><span>{ywmd[0]}</span></div>
                </div>
            
            </div>""",height=100)
        
        scatterPlot()

        if st.sidebar.checkbox('Show data'):
            st.write(df_brand)
        

    else:
        st.header('Please upload your data file')


if __name__=="__main__":
    write()