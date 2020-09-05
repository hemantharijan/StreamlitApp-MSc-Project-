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

from scipy.stats import pearsonr


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

corr = 0.0
def Corr():
    global corr
    year = df_brand['Year_Of_Registration']
    price = df_brand['Price_inEURO']    
    corr,_ = pearsonr(year, price)              #Finding Correlation
    return corr


def write():

    components.html(f"""
             <link href="https://unpkg.com/tailwindcss@^1.0/dist/tailwind.min.css" rel="stylesheet">
                <div class="flex">
                    <div class="flex-auto rounded-md shadow-lg overflow-hidden text-white font-bold rounded-md text-xl bg-blue-500 text-center px-4 py-4 m-2">
                    Price Distribution
                    </div>
                </div>
    """,height=75)

    data = st.sidebar.file_uploader('upload car data file', type='csv')
    
    if data is not None:    
        
        carData(data)
        brandlist = df['Brand'].unique().tolist()
        brandname = st.selectbox('Select car brand',brandlist)
        brand(brandname)

        data_count = df_brand.shape
        ywmd = df_brand.loc[df_brand['Price_inEURO']==df_brand['Price_inEURO'].max()]
        #print(ywmd)
        ywmd = ywmd.values.tolist()

        Corr()
        Menu1 = ["Year to Year","Month wise","Average distribution per year"]
            
        choice = st.sidebar.radio("",list(Menu1))

        if choice == "Year to Year":
            #print(choice)
            components.html(f"""
            <link href="https://unpkg.com/tailwindcss@^1.0/dist/tailwind.min.css" rel="stylesheet">
            <div class="flex rounded-lg shadow-lg overflow-hidden rounded-md bg-blue-500 px-4 py-4">
            <div class="flex flex-wrap gap-x-2  gap-y-2">
    
                <div class="rounded-md bg-white overflow-hidden shadow-lg">
                    <div class="px-6 pt-2">
                        <div class="text-l text-center"><span>Total Count</span></div>
                    </div>
                    <div class="px-6 font-bold text-xl pb-2"><span>{data_count[0]}</span></div>
                </div>
    
                <div class="rounded-md bg-white overflow-hidden shadow-lg">
                    <div class="px-6 pt-2">
                        <div class="text-l text-center"><span>Price Range</span></div>
                    </div>
                    <div class="px-6 font-bold text-xl pb-2"><span>{df_brand['Price_inEURO'].min()} € - {df_brand['Price_inEURO'].max()} €</span></div>
                </div>

                <div class="rounded-md bg-white overflow-hidden shadow-lg">
                    <div class="px-6 pt-2">
                        <div class="text-l text-center"><span>Correlation</span></div>
                    </div>
                    <div class="px-6 font-bold text-xl pb-2"><span>{"{:.3f}".format(corr)}</span></div>
                </div>

                 <div class="overflow-hidden px-6 pt-2">
                    <div >
                        <div class="text-l text-white"><span>Year with max Distribution</span></div>
                    </div>
                    <div class="font-bold text-white text-xl pb-2"><span>{ywmd[0][2]}</span></div>
                </div>

                <div class="overflow-hidden">
                    <div class="px-2 pt-2">
                        <div class="text-l text-white"><span>Model name</span></div>
                    </div>
                    <div class="px-2 font-bold text-white text-xl pb-2"><span>{ywmd[0][1]}</span></div>
                </div>

                <div class="overflow-hidden">
                    <div class="px-2 pt-2">
                        <div class="text-l text-white"><span>Km driven</span></div>
                    </div>
                    <div class="px-2 font-bold text-white text-xl pb-2"><span>{ywmd[0][4]}</span></div>
                </div>
                <div class="overflow-hidden">
                    <div class="px-2 pt-2">
                        <div class="text-l text-white"><span>Current Selling price</span></div>
                    </div>
                    <div class="px-2 font-bold text-white text-xl pb-2"><span>{ywmd[0][5]}</span></div>
                </div>
            </div>
            </div>""",height=180)
            scatterPlot()

        elif choice == "Month wise":
            print(choice)
        elif choice == "Average distribution per year":
            print(choice)
        
        

    else:
        st.header('Please upload your data file')


if __name__=="__main__":
    write()



    