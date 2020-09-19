import streamlit as st
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.figure_factory as ff
import streamlit.components.v1 as components

df_brand_count = st.empty()
df= st.empty()

def data(data):
    global df
    df = pd.read_csv(data,engine="python")
    return 

def Plot_Popular_brand(year):
    global df_brand_count
    df_year = df.loc[df['Year_Of_Registration']==year]
    df_brand_count = pd.DataFrame(df_year['Brand'].value_counts())
    df_brand_count.reset_index(inplace=True)
    df_brand_count.columns = ['Brands','Frequency']
    fig = px.bar(df_brand_count.head(15), x='Brands', y='Frequency',  
                hover_data=['Frequency','Brands'], color='Frequency', height=750
    )
    return st.plotly_chart(fig)
def write():
    
    components.html(f"""
             <link href="https://unpkg.com/tailwindcss@^1.0/dist/tailwind.min.css" rel="stylesheet">
                <div class="flex">
                    <div class="flex-auto rounded-md shadow-lg overflow-hidden text-white font-bold 
                    rounded-md text-xl bg-blue-500 text-center px-4 py-4 m-2">
                    Brands
                    </div>
                </div>
    """,height=75)

    fileupload = st.sidebar.file_uploader('upload car data file', type='csv')

    if fileupload is not None:
        
        data(fileupload)

        menu = ['Popular', 'Premium', 'Non-Premium' ]
        choice = st.sidebar.radio('',menu)

        if choice == 'Popular':
            yearlist = df['Year_Of_Registration'].unique().tolist()
            yearlist.sort()
            year = st.selectbox('Select year',yearlist)
            Plot_Popular_brand(year)

            components.html(f"""
             <link href="https://unpkg.com/tailwindcss@^1.0/dist/tailwind.min.css" rel="stylesheet">
                <div class="flex">
                    
                    <div class="flex-auto rounded-md shadow-lg overflow-hidden text-white font-bold 
                    rounded-md text-xl bg-blue-500 text-center px-4 py-4 m-2">
                    
                     <div class="flex justify-center  gap-x-2">
                    
                    <div class="max-w-sm overflow-hidden rounded-md shadow-lg bg-white">
                        <div class="text-md text-blue-500 px-8 pt-4">Positive Statements</div>
                        <div class="text-center font-bold text-2xl pb-2 text-blue-500">
                            <span>20</span>
                        </div>
                    </div>

                    <div class="max-w-sm overflow-hidden rounded-md shadow-lg">
                        <div class="text-md px-8 pt-4">Negative Statements</div>
                        <div class="text-center font-bold text-2xl pb-2 text-red-500">
                            <span>30</span>
                        </div>
                    </div>

                    <div class="max-w-sm overflow-hidden rounded-md shadow-lg">
                        <div class="text-md px-8 pt-4">Neutral Statements</div>
                        <div class="text-center font-bold text-2xl pb-2 text-gray-500">
                            <span>40</span>
                        </div>
                    </div>
                </div>
                    </div>
                </div>
            """,height=200)

        elif choice == 'Premium':
            print("Yo")
        
        elif choice == 'Non-Premium':
            print("Ho")

    else:
        st.subheader('Upload data file!!')
if __name__=="__main__":
    write()
