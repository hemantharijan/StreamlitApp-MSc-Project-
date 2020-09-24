import streamlit as st
import awesome_streamlit as ast
import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import pickle
import time
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

#..................................................Logic....................................................#

df_car = pd.DataFrame()

pred_price = 0

def data(file):
    global df_car
    df_car = pd.read_csv(file, engine='python')
    return

def price_pred(brand, yor, kmdriven, powerps, gearbox, fueltype, vehicletype):

    global pred_price
    
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
    
    print('Brand label: '+str(brand_dict[brand])+' yor '+ str(yor) +' km '+ str(kmdriven) +' powerps '+ str(powerps) 
            +' gearbox '+ str(gearbox_dict[gearbox]) +' fueltype '+ str(FuelType_dict[fueltype]) +' vehicletype '
            + str(VehicleType_dict[vehicletype]))

    #Droping nominal datas
    df_pred = pd.DataFrame(df_car)
    df_pred.drop(['srno','Brand','Month_Of_Registration','Model','GearBox','FuelType','VehicleType','MOR label'],
                    inplace=True, axis=1)
    df_pred.fillna(0, inplace=True)
    
    #Collecting X and y data for training
    X_Car = df_pred.drop('Price_inEURO', axis=1)
    y_Car = df_pred['Price_inEURO']
    
    #spliting into train and test
    X_train, X_test, y_train, y_test = train_test_split(X_Car, y_Car, test_size = 0.25, random_state=0)

    sc = StandardScaler()
    X_train_scaled = sc.fit_transform(X_train)
    X_test_scaled = sc.transform(X_test)

    #XGBooster algorithm
    start = time.time()
    filename = r"models\xgbreg.pkl"
    load_model = pickle.load(open(filename,'rb'))

    #User defined features
    example_car = [[brand_dict[brand], yor, kmdriven, powerps, gearbox_dict[gearbox], FuelType_dict[fueltype], 
                    VehicleType_dict[vehicletype]]]
    example_car_scaled = sc.transform(example_car)
    print('Predicted Car price is ', load_model.predict(example_car_scaled))
    end = time.time()
    print(f"{end - start}")
    pred_price =load_model.predict(example_car_scaled)
    return


#..................................................User-Interface....................................................#
def write():
    
    file = st.sidebar.file_uploader('upload car data file', type='csv')

    components.html(f"""
             <link href="https://unpkg.com/tailwindcss@^1.0/dist/tailwind.min.css" rel="stylesheet">
                <div class="flex">
                    <div class="flex-auto rounded-md shadow-lg overflow-hidden text-gray-400 font-bold 
                    rounded-md text-xl border-2 border-blue-500 text-center px-4 py-4 m-2">
                    Get Price 
                    </div>
                </div>
    """,height=90)

    if file is not None:
        data(file)
        
        brandlist = df_car['Brand'].unique().tolist()
        brandlist.sort()
        brandname = st.selectbox('Brand',brandlist)
        
        yorlist = df_car['Year_Of_Registration'].unique().tolist()
        yorlist.sort()
        year = st.selectbox('Year Of Registration',yorlist)

        kmDriven = st.number_input('Km Driven', min_value= 0.0, max_value= 200000.0)
        powerPS = st.number_input('PowerPS', min_value=0.0, max_value=1500.0)
        
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
            if powerPS != 0 or kmDriven != 0:
                components.html(f"""
                    <link href="https://unpkg.com/tailwindcss@^1.0/dist/tailwind.min.css" rel="stylesheet">
                    <div class = "flex gap-x-4">
                        
                        <div class="flex flex-wrap rounded-lg overflow-hidden gap-x-2 shadow-lg bg-blue-500 px-4 py-4">
                            <span class="text-white text-xl pt-2">Predicted Price is:&nbsp&nbsp</span>
                            <div class="rounded-lg shadow-lg bg-white px-2 overflow-hidden py-2">
                                <span class="text-blue-500 text-xl font-bold">{"{:.2f}".format(pred_price[0])} €</span>
                            </div>
                        </div>
                    </div>
                    """)
            else:
                components.html(f"""
                    <link href="https://unpkg.com/tailwindcss@^1.0/dist/tailwind.min.css" rel="stylesheet">
                    <div class = "flex gap-x-4">
                        
                        <div class="flex flex-wrap rounded-lg overflow-hidden gap-x-2 shadow-lg bg-red-500 px-4 py-4">
                            <span class="text-white text-xl">Km Driven or PowerPS cannot be zero</span>
                        </div>
                    </div>
                    """)
    else:
        st.subheader('Upload data file!!')

if __name__ == '__main__':
    write()