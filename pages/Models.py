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

def year_to_year(brand_name, model_name):
    
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
        font_color="#2ED9FF",
        font_size=14
    )

    return st.plotly_chart(fig) 


def trend(brand_name):
    car_brand = pd.DataFrame(df.query('Brand == "'+brand_name+'"'))
    car_brand.dropna(inplace=True)
    car_brand.head(5)
    model_label = car_brand['Model'].unique().tolist()

    for index, model in enumerate(model_label):
        if(model=='not available'):
            model_label.pop(index)

    x_data = []
    y_data = []
    for model in model_label:
        
        car_model = pd.DataFrame(car_brand.query('Model == "'+model+'"'))
        yearlist = car_model['Year_Of_Registration'].unique().tolist()
        yearlist.sort()
        x_data.append(yearlist)
        
        yearcount = pd.DataFrame(car_model['Year_Of_Registration'].value_counts())
        yearcount.sort_index(inplace = True)
        y_count = yearcount['Year_Of_Registration'].tolist()
        y_data.append(y_count)

    fig1 = go.Figure()

    for i in range(0, len(model_label)):
        fig1.add_trace(go.Scatter(x=x_data[i], y=y_data[i], 
                                mode='lines+markers',
                                name=model_label[i]))
        fig1.add_trace(go.Scatter(
            x=[x_data[i][0], x_data[i][-1]],
            y=[y_data[i][0], y_data[i][-1]],
            mode='markers',
        ))
        fig1.update_layout(hovermode='x unified')
        
    fig1.update_layout(
    paper_bgcolor='rgb(40,44,53)',
    plot_bgcolor='rgb(40,44,53)',
    font_color="#2ED9FF",
    font_size=14,
    height=620, width=1100,
    hoverlabel=dict(
        font_size=20,
        font_family="Rockwell"
    ),
    xaxis=dict(
        showgrid=False
    ),
    yaxis=dict(
        zeroline=False,
        showline=False,
    ),)
    return st.plotly_chart(fig1) 

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

        menu = ['Sales','Trend']

        choice = st.sidebar.selectbox('',menu)

        if choice == 'Sales':
            st.subheader('Car Brand')
            brand_name = st.selectbox('',brand_list)
            
            model_list = df['Model'].where(df['Brand']==brand_name).unique().tolist()
            
            for index, model in enumerate(model_list):
                if(pd.isnull(model) or model == 'not available'):
                    model_list.pop(index)
            st.subheader('Brand Model')
            model_name = st.selectbox('',model_list)
            
            year_to_year(brand_name, model_name)

        elif choice == 'Trend':
            st.subheader('Car Brand')
            brand_name = st.selectbox('',brand_list)
            trend(brand_name)

    
    else:
        st.subheader('Upload data File!!')
        

if __name__=="__main__":
    write()