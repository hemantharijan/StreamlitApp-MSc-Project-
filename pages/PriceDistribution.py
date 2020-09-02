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
        
        if st.sidebar.checkbox('Show data'):
            st.write(df_brand)
        data_count = df_brand.shape
        
        components.html(f"""
            <link href="https://unpkg.com/tailwindcss@^1.0/dist/tailwind.min.css" rel="stylesheet">

            <div class="flex flex-wrap">
    
                <div class="max-w-sm rounded overflow-hidden shadow-lg">
                    <div class="px-6 py-4">
                        <div class="font-bold text-xl mb-2"><span>Total Count</span></div>
                    </div>
                    <div class="px-6 pt-4 pb-2"><span>{data_count[0]}</span></div>
                </div>
    
                <div class="max-w-sm rounded overflow-hidden shadow-lg">
                    <div class="px-6 py-4">
                        <div class="font-bold text-xl mb-2"><span>Max Price</span></div>
                    </div>
                    <div class="px-6 pt-4 pb-2"><span>{df_brand['Price_inEURO'].max()} €</span></div>
                </div>
    
                <div class="max-w-sm rounded overflow-hidden shadow-lg">
                    <div class="px-6 py-4">
                        <div class="font-bold text-xl mb-2"><span>Min Price</span></div>
                    </div>
                    <div class="px-6 pt-4 pb-2"><span>{df_brand['Price_inEURO'].min()} €</span></div>
                </div>
            
            </div>""")
        
        scatterPlot()

    else:
        st.header('Please upload your data file')


if __name__=="__main__":
    write()