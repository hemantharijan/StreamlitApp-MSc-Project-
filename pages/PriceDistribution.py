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
def carData(file):
    global df
    df = pd.read_csv(file,engine="python")
    df= df.set_index('srno')
    return

df_brand = pd.DataFrame()
def brand(brandname):
    global df_brand
    df_brand= df.loc[df['Brand']==brandname]
    return 

df_brand_year = pd.DataFrame()
def month_wise(brand, year):
    global df_brand_year
    df_brand_year = df.query('Brand == "'+brand+'" and Year_Of_Registration == '+str(year))
    return


def scatterPlot(x_variable, y_variable):
    fig = go.Figure(data=go.Scatter(
    x= x_variable,
    y= y_variable,
    mode='markers',
    #height=700,
    marker=dict(
        size=8,
        color= df_brand['Price_inEURO'], 
        colorscale='Viridis',
        showscale=True
    )))
    fig.update_layout(
        xaxis_title='Year of Registration',
        yaxis_title='Price in EURO')
    return st.plotly_chart(fig)

year_price_corr = 0.0
def YearCorr():
    global year_price_corr
    year = df_brand['Year_Of_Registration']
    price = df_brand['Price_inEURO']    
    year_price_corr,_ = pearsonr(year, price)              #Finding Correlation
    return 

month_price_corr = 0.0
def monthCorr():
    global month_price_corr
    year = df_brand['MOR label']
    price = df_brand['Price_inEURO']    
    month_price_corr,_ = pearsonr(year, price)              #Finding Correlation
    return 



def write():

    components.html(f"""
             <link href="https://unpkg.com/tailwindcss@^1.0/dist/tailwind.min.css" rel="stylesheet">
                <div class="flex">
                    <div class="flex-auto rounded-md shadow-lg overflow-hidden text-white font-bold rounded-md text-xl bg-blue-500 text-center px-4 py-4 m-2">
                    Price Distribution
                    </div>
                </div>
    """,height=75)

    file = st.sidebar.file_uploader('upload car data file', type='csv')
    
    if file is not None:    
        
        carData(file)
        brandlist = df['Brand'].unique().tolist()
        #sorted_brandlist=brandlist.sort()
        brandlist.sort()
        brandname = st.selectbox('Select car brand',brandlist)
        brand(brandname)

        brand_count = df_brand.shape
        ywmd = df_brand.loc[df_brand['Price_inEURO']==df_brand['Price_inEURO'].max()]
        print(ywmd)
        ywmd = ywmd.values.tolist()

        YearCorr()
        Menu1 = ["Year to Year","Month wise","Average distribution per year"]
            
        choice = st.sidebar.radio("",Menu1)

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
                    <div class="px-6 font-bold text-xl pb-2"><span>{brand_count[0]}</span></div>
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
                    <div class="px-6 font-bold text-xl pb-2"><span>{"{:.3f}".format(year_price_corr)}</span></div>
                </div>

                 <div class="overflow-hidden px-6 pt-2">
                    <div >
                        <div class="text-l text-white"><span>Year with max Distribution</span></div>
                    </div>
                    <div class="font-bold text-white text-xl pb-2"><span>{ywmd[0][3]}</span></div>
                </div>

                <div class="overflow-hidden">
                    <div class="px-2 pt-2">
                        <div class="text-l text-white"><span>Model name</span></div>
                    </div>
                    <div class="px-2 font-bold text-white text-xl pb-2"><span>{ywmd[0][2]}</span></div>
                </div>

                <div class="overflow-hidden">
                    <div class="px-2 pt-2">
                        <div class="text-l text-white"><span>Km driven</span></div>
                    </div>
                    <div class="px-2 font-bold text-white text-xl pb-2"><span>{ywmd[0][5]}</span></div>
                </div>
                <div class="overflow-hidden">
                    <div class="px-2 pt-2">
                        <div class="text-l text-white"><span>Current Selling price</span></div>
                    </div>
                    <div class="px-2 font-bold text-white text-xl pb-2"><span>{ywmd[0][6]} €</span></div>
                </div>
            </div>
            </div>""",height=180)

            year_of_registration = df_brand["Year_Of_Registration"]
            price = df_brand['Price_inEURO']
            scatterPlot(year_of_registration, price)

        elif choice == "Month wise":
            #print(choice)
            yearlist = df_brand['Year_Of_Registration'].unique().tolist()
            yearlist.sort()
            Reg_year = st.selectbox("Select Year of registration",yearlist)
            
            month_wise(brandname, Reg_year)
            
            monthCorr()

            month_count = df_brand_year.shape

            mwmd = df_brand_year.loc[df_brand_year['Price_inEURO']==df_brand_year['Price_inEURO'].max()]
            mwmd = mwmd.values.tolist()
            print(mwmd)
            components.html(f"""
            <link href="https://unpkg.com/tailwindcss@^1.0/dist/tailwind.min.css" rel="stylesheet">
            <div class="flex rounded-lg shadow-lg overflow-hidden rounded-md bg-blue-500 px-4 py-4">
            <div class="flex flex-wrap gap-x-2  gap-y-2">
    
                <div class="rounded-md bg-white overflow-hidden shadow-lg">
                    <div class="px-6 pt-2">
                        <div class="text-l text-center"><span>Total Count</span></div>
                    </div>
                    <div class="px-6 font-bold text-xl pb-2"><span>{month_count[0]}</span></div>
                </div>
    
                <div class="rounded-md bg-white overflow-hidden shadow-lg">
                    <div class="px-6 pt-2">
                        <div class="text-l text-center"><span>Price Range</span></div>
                    </div>
                    <div class="px-6 font-bold text-xl pb-2"><span>{df_brand_year['Price_inEURO'].min()} € - {df_brand_year['Price_inEURO'].max()} €</span></div>
                </div>

                <div class="rounded-md bg-white overflow-hidden shadow-lg">
                    <div class="px-6 pt-2">
                        <div class="text-l text-center"><span>Correlation</span></div>
                    </div>
                    <div class="px-6 font-bold text-xl pb-2"><span>{"{:.3f}".format(month_price_corr)}</span></div>
                </div>

                 <div class="overflow-hidden px-4 pt-2">
                    <div >
                        <div class="text-l text-white"><span>Month with max Distribution</span></div>
                    </div>
                    <div class="font-bold text-white text-xl pb-2"><span>{mwmd[0][4]}</span></div>
                </div>

                <div class="overflow-hidden">
                    <div class="px-2 pt-2">
                        <div class="text-l text-white"><span>Model name</span></div>
                    </div>
                    <div class="px-2 font-bold text-white text-xl pb-2"><span>{mwmd[0][2]}</span></div>
                </div>

                <div class="overflow-hidden">
                    <div class="px-2 pt-2">
                        <div class="text-l text-white"><span>Km driven</span></div>
                    </div>
                    <div class="px-2 font-bold text-white text-xl pb-2"><span>{mwmd[0][5]}</span></div>
                </div>
                <div class="overflow-hidden">
                    <div class="px-2 pt-2">
                        <div class="text-l text-white"><span>Current Selling price</span></div>
                    </div>
                    <div class="px-2 font-bold text-white text-xl pb-2"><span>{mwmd[0][6]} €</span></div>
                </div>
            </div>
            </div>""",height=180)

            month_of_registration = df_brand_year["Month_Of_Registration"]
            price = df_brand_year['Price_inEURO']
            scatterPlot(month_of_registration, price)
            

        elif choice == "Average distribution per year":
            
            years = df['Year_Of_Registration'].unique()
            print(years)
            avg_price = []
            for year in years:
                df_year = df_brand.query('Year_Of_Registration == '+str(year))
                avg = np.average(df_year['Price_inEURO'])
                avg_price.append(avg)

            data = {'Years':years, 'Average Price':avg_price}
            avg_df = pd.DataFrame(data)
            avg_df.sort_values(by='Years',inplace=True)

            components.html(f"""
            <link href="https://unpkg.com/tailwindcss@^1.0/dist/tailwind.min.css" rel="stylesheet">
            <div class="flex justify-center">
            <div class="rounded-lg shadow-lg overflow-hidden rounded-md bg-blue-500 px-4 py-4">
            <div class="flex flex-wrap gap-x-2  gap-y-2">
    
                <div class="rounded-md bg-white overflow-hidden shadow-lg">
                    <div class="px-6 pt-2">
                        <div class="text-l text-center"><span>Min Average</span></div>
                    </div>
                    <div class="px-6 font-bold text-xl pb-2">
                    <span>{"{:.2f}".format(avg_df['Average Price'].min())}</span>
                    </div>
                </div>
    
                <div class="rounded-md bg-white overflow-hidden shadow-lg">
                    <div class="px-6 pt-2">
                        <div class="text-l text-center"><span>Max Average</span></div>
                    </div>
                    <div class="px-6 font-bold text-xl pb-2"><span>{"{:.2f}".format(avg_df['Average Price'].max())}</span></div>
                </div>
            </div>
            </div>
            </div>""",height=110)

           
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=avg_df['Years'], y=avg_df['Average Price'],
                    mode='lines+markers',
                    name='lines+markers'))
            fig.update_layout(
                xaxis_title ='Year of registration',
                yaxis_title ='Average Price',
                width = 750,
                height = 380
            )
            st.plotly_chart(fig)

    else:
        st.subheader('Upload data file!!')

if __name__=="__main__":
    write()



    