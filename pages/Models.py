import streamlit as st
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import streamlit.components.v1 as components

df= st.empty()
brand_list = []

def data(data):
    
    global df, brand_list
    df = pd.read_csv(data,engine="python")
    brand_list = df['Brand'].unique().tolist()
    return 



def models(brand_name, model_name):
    
    df_brand = df.query('Brand == "'+brand_name+'" ')
    df_model = df_brand.query('Model == "'+model_name+'" ')
    
    df_model_data = pd.DataFrame(df_model['Year_Of_Registration'].value_counts())
    df_model_data.reset_index(inplace = True)
    df_model_data.columns = ['Years','Model sold']  
    df_model_data.sort_values(by=['Years'], inplace=True)
    
    fig = px.bar(df_model_data, x='Years', y='Model sold',  
            hover_data=['Years','Model sold'], color='Model sold', height=620, width=1100
    )
    fig.update_layout(   
        paper_bgcolor='rgb(40,44,53)',
        plot_bgcolor='rgb(40,44,53)',
        font_color="white"
    )

    return st.plotly_chart(fig) 




def write():

    components.html(f"""
             <link href="https://unpkg.com/tailwindcss@^1.0/dist/tailwind.min.css" rel="stylesheet">
                <div class="flex">
                    <div class="flex-auto rounded-md shadow-lg overflow-hidden text-gray-400 font-bold 
                    rounded-md text-xl border-2 border-blue-500 text-center px-4 py-4 m-2">
                    Year to Year Sales
                    </div>
                </div>
    """,height=90)

    fileupload = st.sidebar.file_uploader('upload car data file', type='csv')

    if fileupload is not None:
        
        data(fileupload)

        brand_name = st.selectbox('select brand',brand_list)
        
        model_list = df['Model'].where(df['Brand']==brand_name).unique().tolist()
        
        for index, model in enumerate(model_list):
            if(pd.isnull(model) or model == 'not available'):
                model_list.pop(index)
        
        model_name = st.selectbox('select model',model_list)
        
        models(brand_name, model_name)

if __name__=="__main__":
    write()