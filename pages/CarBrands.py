import streamlit as st
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
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
                hover_data=['Frequency','Brands'], color='Frequency', height=620, width=1100
    )
    fig.update_layout(
        paper_bgcolor='rgb(40,44,53)',
        plot_bgcolor='rgb(40,44,53)',
        font_color="#2ED9FF",
        font_size=14
    )
    return st.plotly_chart(fig)

def write():
    
    st.write(
        """<style type="text/css" media="screen">
            div[role="listbox"] ul {
            height:300px;
            color: white;}
        </style>
        """,
        unsafe_allow_html=True,
    )

    components.html(f"""
             <link href="https://unpkg.com/tailwindcss@^1.0/dist/tailwind.min.css" rel="stylesheet">
                <div class="flex">
                    <div class="flex-auto rounded-md shadow-lg overflow-hidden text-gray-400 font-bold 
                    rounded-md text-xl border-2 border-blue-500 text-center px-4 py-4 m-2">
                    Year to Year popularity and class
                    </div>
                </div>
    """,height=90)

    fileupload = st.sidebar.file_uploader('upload car data file', type='csv')

    if fileupload is not None:
        
        data(fileupload)

        menu = ['Popular', 'Class' ]
        choice = st.sidebar.radio('',menu)

        if choice == 'Popular':
            yearlist = df['Year_Of_Registration'].unique().tolist()
            yearlist.sort()
            st.subheader('Year')
            year = st.selectbox('',yearlist)
            Plot_Popular_brand(year)
        
            top_three_brands = df_brand_count['Brands'].loc[0:2].tolist()
            top_three_brands_freq = df_brand_count['Frequency'].loc[0:2].tolist()

            components.html(f"""
             <link href="https://unpkg.com/tailwindcss@^1.0/dist/tailwind.min.css" rel="stylesheet">
                <div class="flex">
                    
                    <div class="flex-auto rounded-md shadow-md overflow-hidden rounded-md text-center px-4 py-4 m-2">
                    <span class="text-blue-500">Top three popular brands with no of cars sold in year {year}</span>
                    <div class="flex justify-center pt-2 gap-x-4">

                    <div class="max-w-sm overflow-hidden rounded-md shadow-md">
                        <div class="text-md text-blue-500 font-bold px-8 text-xl pt-4">{top_three_brands[0]}</div>
                        <div class="text-center text-lg pb-2 text-blue-500">
                            <span>{top_three_brands_freq[0]}</span>
                        </div>
                    </div>

                    <div class="max-w-sm overflow-hidden rounded-md shadow-md">
                       <div class="text-md text-blue-500 font-bold px-8 text-xl pt-4">{top_three_brands[1]}</div>
                        <div class="text-center text-lg pb-2 text-blue-500">
                            <span>{top_three_brands_freq[1]}</span>
                        </div>
                    </div>

                    <div class="max-w-sm overflow-hidden rounded-md shadow-md">
                        <div class="text-md text-blue-500 font-bold px-8 text-xl pt-4">{top_three_brands[2]}</div>
                        <div class="text-center text-lg pb-2 text-blue-500">
                            <span>{top_three_brands_freq[2]}</span>
                        </div>
                    </div>
                </div>
                    </div>
                </div>
            """,height=200)

        elif choice == 'Class':           

            labels = ['Standard','Luxury','Ultra Luxury']
            values = [72772, 120877, 25701]
            fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5)])
            fig.update_layout(
                height=700,
                width=1000,
                paper_bgcolor='rgb(40,44,53)',
                plot_bgcolor='rgb(40,44,53)',
                font_color="white"
            )
            st.plotly_chart(fig)

    else:
        st.subheader('Upload data file!!')

if __name__=="__main__":
    write()
