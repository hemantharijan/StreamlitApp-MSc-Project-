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


df = pd.DataFrame()
def data(file):
    global df
    df = pd.read_csv(file, engine='python')
    return

def price_pred(brand, yor, kmdriven, powerps, gearbox, fueltype, vehicletype, ):
    
    #Brand label list
    df_brand_list = df['Brand'].unique()
    df_brand_label_list = df['Brand label'].unique()
    brand_dict = {df_brand_list[i]: df_brand_label_list[i] for i in range(len(df_brand_list))}

    #Gearbox
    df_GearBox_list = df['GearBox'].unique().tolist()
    df_GearBox_list.pop(2)
    df_GearBox_label_list = df['GearBox label'].unique().tolist()
    df_GearBox_label_list.pop(2)
    gearbox_dict = {df_GearBox_list[i]:df_GearBox_label_list[i] for i in range(len(df_GearBox_list))}
    
    #FuelType
    df_FuelType_list = df['FuelType'].unique().tolist()
    df_FuelType_list.pop(2)
    df_FuelType_label_list = df['FuelType label'].unique().tolist()
    df_FuelType_label_list.pop(2)
    FuelType_dict = {df_FuelType_list[i]:df_FuelType_label_list[i] for i in range(len(df_FuelType_list))}

    #VehicleType
    df_VehicleType_list = df['VehicleType'].unique().tolist()
    df_VehicleType_list.pop(6)
    df_VehicleType_label_list = df['VehicleType label'].unique().tolist()
    df_VehicleType_label_list.pop(6)
    VehicleType_dict = {df_VehicleType_list[i]:df_VehicleType_label_list[i] for i in range(len(df_VehicleType_list))}
    
    print('Brand label: '+str(brand_dict[brand])+' yor '+ str(yor) +' km '+ str(kmdriven) +' powerps '+ str(powerps) +' gearbox '+ str(gearbox_dict[gearbox]) +' fueltype '+ str(FuelType_dict[fueltype]) +' vehicletype '+ str(VehicleType_dict[vehicletype]))

    return

def write():
    
    file = st.sidebar.file_uploader('upload car data file', type='csv')

    components.html(f"""
             <link href="https://unpkg.com/tailwindcss@^1.0/dist/tailwind.min.css" rel="stylesheet">
                <div class="flex">
                    <div class="flex-auto rounded-md shadow-lg overflow-hidden text-white font-bold rounded-md text-xl bg-blue-500 text-center px-4 py-4 m-2">
                    Price Predictor
                    </div>
                </div>
    """,height=75)

    if file is not None:
        data(file)
        
        brandlist = df['Brand'].unique().tolist()
        brandlist.sort()
        brandname = st.selectbox('Brand',brandlist)
        
        yorlist = df['Year_Of_Registration'].unique().tolist()
        yorlist.sort()
        year = st.selectbox('Year Of Registration',yorlist)

        kmDriven = st.number_input('Km Driven')
        powerPS = st.number_input('PowerPS')
        
        gearboxlist = df['GearBox'].unique().tolist()
        gearboxlist.pop(2)
        gearbox = st.selectbox('GearBox',gearboxlist)

        fueltypelist = df['FuelType'].unique().tolist()
        fueltype = st.selectbox('FuelType',fueltypelist)
        
        vehicletypelist = df['VehicleType'].unique().tolist()
        vehicletypelist.pop(6)
        vehicletype = st.selectbox('VehicleType',vehicletypelist)
        
        if st.button('Predict'):
            price_pred(brandname, year, kmDriven, powerPS, gearbox, fueltype, vehicletype)
        
    else:
        st.subheader('Upload data file!!')

if __name__ == '__main__':
    write()