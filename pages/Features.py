import streamlit as st
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import streamlit.components.v1 as components
from plotly.subplots import make_subplots

def data(data):
    
    df = pd.read_csv(data,engine="python")
    
    Fuel_Label = df['FuelType'].unique().tolist()
    Gear_Label = df['GearBox'].unique().tolist()
    Vehicle_Label = df['VehicleType'].unique().tolist()

    Labels = [Fuel_Label, Gear_Label, Vehicle_Label]

    for label in Labels:
        for index, lbl in enumerate(label):
            if(pd.isnull(lbl)):
                label.pop(index)

    # Create subplots: use 'domain' type for Pie subplot
    fig = make_subplots(rows=1, cols=3, specs=[[{'type':'domain'}, {'type':'domain'},{'type':'domain'} ]])
    
    fig.add_trace(go.Pie(labels= Fuel_Label, values=[93759, 127159, 3318, 123, 255, 492]), 1, 1)
    fig.add_trace(go.Pie(labels=Gear_Label, values=[172609,57975]), 1, 2)
    fig.add_trace(go.Pie(labels=Vehicle_Label, values=[10733, 12009, 48956, 14968, 23816, 108868]), 1, 3)
    fig.update_traces(hole=.7)

    fig.update(layout_showlegend=False)
    fig.update_layout(height=450,width=1100, font_color='white', paper_bgcolor='rgb(40,44,53)', plot_bgcolor='rgb(40,44,53)')

    return st.plotly_chart(fig)

def write():
    
    components.html(f"""
             <link href="https://unpkg.com/tailwindcss@^1.0/dist/tailwind.min.css" rel="stylesheet">
                <div class="flex">
                    <div class="flex-auto rounded-md shadow-lg overflow-hidden text-gray-400 font-bold 
                    rounded-md text-xl border-2 border-blue-500 text-center px-4 py-4 m-2">
                    Feature Analysis
                    </div>
                </div>
    """,height=90)

    fileupload = st.sidebar.file_uploader('upload car data file', type='csv')

    if fileupload is not None:     
        data(fileupload)

        components.html(f"""
        <link href="https://unpkg.com/tailwindcss@^1.0/dist/tailwind.min.css" rel="stylesheet">
        <div class="flex flex-auto justify-center -ml-5 my-8 gap-x-64 -my-4">
            <div class="text-center border-2 border-blue-500 text-blue-500 px-4 ml-8 py-4 z-0 font-bold rounded-md shadow-xl">Fuel Type</div>
            <div class="text-center border-2 border-blue-500 text-blue-500 px-4 py-4 -ml-8 z-10 font-bold rounded-md shadow-xl">Gear Box</div>
            <div class="text-center border-2 border-blue-500 text-blue-500 px-4 py-4 -ml-8 font-bold z-20 rounded-md shadow-xl">Vehicle Type</div>
        </div>
    """)


if __name__=="__main__":
    write()