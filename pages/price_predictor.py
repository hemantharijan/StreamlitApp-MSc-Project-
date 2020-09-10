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
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import MinMaxScaler


df_car = pd.DataFrame()
def data(file):
    global df_car
    df_car = pd.read_csv(file, engine='python')
    return

pred_price = 0
accuracy = 0
def price_pred(brand, yor, kmdriven, powerps, gearbox, fueltype, vehicletype):

    global pred_price, accuracy
    
    #Brand label list
    df_brand_list = df_car['Brand'].unique()
    df_brand_label_list = df_car['Brand label'].unique()
    brand_dict = {df_brand_list[i]: df_brand_label_list[i] for i in range(len(df_brand_list))}

    #Gearbox
    df_GearBox_list = df_car['GearBox'].unique().tolist()
    df_GearBox_list.pop(2)
    df_GearBox_label_list = df_car['GearBox label'].unique().tolist()
    df_GearBox_label_list.pop(2)
    gearbox_dict = {df_GearBox_list[i]:df_GearBox_label_list[i] for i in range(len(df_GearBox_list))}
    
    #FuelType
    df_FuelType_list = df_car['FuelType'].unique().tolist()
    df_FuelType_list.pop(2)
    df_FuelType_label_list = df_car['FuelType label'].unique().tolist()
    df_FuelType_label_list.pop(2)
    FuelType_dict = {df_FuelType_list[i]:df_FuelType_label_list[i] for i in range(len(df_FuelType_list))}

    #VehicleType
    df_VehicleType_list = df_car['VehicleType'].unique().tolist()
    df_VehicleType_list.pop(6)
    df_VehicleType_label_list = df_car['VehicleType label'].unique().tolist()
    df_VehicleType_label_list.pop(6)
    VehicleType_dict = {df_VehicleType_list[i]:df_VehicleType_label_list[i] for i in range(len(df_VehicleType_list))}
    
    print('Brand label: '+str(brand_dict[brand])+' yor '+ str(yor) +' km '+ str(kmdriven) +' powerps '+ str(powerps) +' gearbox '+ str(gearbox_dict[gearbox]) +' fueltype '+ str(FuelType_dict[fueltype]) +' vehicletype '+ str(VehicleType_dict[vehicletype]))

    df_pred = pd.DataFrame(df_car)
    df_pred.drop(['Brand','Month_Of_Registration','Model','GearBox','FuelType','VehicleType','MOR label'], inplace=True, axis=1)
    df_pred.fillna(0, inplace=True)

    car_features = ['Brand label','Year_Of_Registration','Km_Driven','PowerPS','GearBox label','FuelType label','VehicleType label']

    X_Car = df_pred[car_features]
    y_Car = df_pred['Brand label']
    target_car = df_pred.Price_inEURO.values

    X_train, X_test, y_train, y_test = train_test_split(X_Car, y_Car, random_state=10)

    scaler = MinMaxScaler()

    X_train_scale = scaler.fit_transform(X_train)
    X_test_scale = scaler.transform(X_test)

    knn = KNeighborsClassifier(n_neighbors=100)
    #knn = KNeighborsClassifier(n_neighbors = 5)

    knn.fit(X_train_scale, y_train)

    print('Accuracy of K-NN classifier on training set: {:.2f}'
        .format(knn.score(X_train_scale, y_train)))
    print('Accuracy of K-NN classifier on test set: {:.2f}' 
        .format(knn.score(X_test_scale, y_test)))

    example_car = [[brand_dict[brand], yor, kmdriven, powerps, gearbox_dict[gearbox], FuelType_dict[fueltype], VehicleType_dict[vehicletype]]]
    example_car_scaled = scaler.transform(example_car)
    print('Predicted Car price is ', target_car[knn.predict(example_car_scaled)[0]-1])

    accuracy = "{:.2f}".format(knn.score(X_test_scale, y_test)*100)
    pred_price = target_car[knn.predict(example_car_scaled)[0]-1]
    accuracy = accuracy
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
        
        brandlist = df_car['Brand'].unique().tolist()
        brandlist.sort()
        brandname = st.selectbox('Brand',brandlist)
        
        yorlist = df_car['Year_Of_Registration'].unique().tolist()
        yorlist.sort()
        year = st.selectbox('Year Of Registration',yorlist)

        kmDriven = st.number_input('Km Driven')
        powerPS = st.number_input('PowerPS')
        
        gearboxlist = df_car['GearBox'].unique().tolist()
        gearboxlist.pop(2)
        gearbox = st.selectbox('GearBox',gearboxlist)

        fueltypelist = df_car['FuelType'].unique().tolist()
        fueltypelist.pop(2)
        fueltype = st.selectbox('FuelType',fueltypelist)
        
        vehicletypelist = df_car['VehicleType'].unique().tolist()
        vehicletypelist.pop(6)
        vehicletype = st.selectbox('VehicleType',vehicletypelist)
      
        if st.button('Predict'):
            price_pred(brandname, year, kmDriven, powerPS, gearbox, fueltype, vehicletype)
            components.html(f"""
                <link href="https://unpkg.com/tailwindcss@^1.0/dist/tailwind.min.css" rel="stylesheet">
                <div class = "flex gap-x-4">
                    
                    <div class="flex flex-wrap rounded-lg overflow-hidden gap-x-2 shadow-lg bg-blue-500 px-4 py-4">
                        <span class="text-white text-xl pt-2">Predicted Price is:&nbsp&nbsp</span>
                        <div class="rounded-lg shadow-lg bg-white px-2 overflow-hidden py-2">
                            <span class="text-blue-500 text-xl font-bold">{pred_price} €</span>
                        </div>
                    </div>

                    <div class="flex flex-wrap rounded-lg overflow-hidden gap-x-2 shadow-lg bg-green-300 px-4 py-4">
                        <span class="text-white text-xl pt-2">Accuracy on dataset:&nbsp&nbsp</span>
                        <div class="rounded-lg shadow-lg bg-white px-2 overflow-hidden py-2">
                            <span class="text-green-500 text-xl font-bold">{accuracy} %</span>
                        </div>
                    </div>

                </div>
                """)
              
    else:
        st.subheader('Upload data file!!')

if __name__ == '__main__':
    write()