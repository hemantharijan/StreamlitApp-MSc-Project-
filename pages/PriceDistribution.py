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

#..................................................Logic....................................................#
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
    marker=dict(
        size=10,
        color= df_brand['Price_inEURO'], 
        colorscale='Tealgrn',
        showscale=True
    )))
    fig.update_layout(
        xaxis_title='Year of Registration',
        yaxis_title='Price in EURO',
        paper_bgcolor='rgb(40,44,53)',
        plot_bgcolor='rgb(40,44,53)',
        font_color="#1CFFCE",
        font_size=13,
        height=700,
        width=1100,)
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
    mor = df_brand['MOR label']
    price = df_brand['Price_inEURO']    
    month_price_corr,_ = pearsonr(mor, price)              #Finding Correlation
    return 

#..................................................User-Interface....................................................#

def write():

    st.write(
        """
        <style type="text/css" media="screen">
        div[role="listbox"] ul {
            height:300px;
            color:white;
        }
        </style>
        """
        ,
        unsafe_allow_html=True,
    )

    components.html(f"""
             <link href="https://unpkg.com/tailwindcss@^1.0/dist/tailwind.min.css" rel="stylesheet">
                <div class="flex">
                    <div class="flex-auto rounded-md shadow-lg overflow-hidden text-gray-400 font-bold 
                    rounded-md text-xl border-2 border-blue-500 text-center px-4 py-4 m-2">
                    Price Analysis
                    </div>
                </div>
    """,height=90)

    file = st.sidebar.file_uploader('upload car data file', type='csv')
    
    if file is not None:    
        
        carData(file)
        st.subheader('Car Brand')
        brandlist = df['Brand'].unique().tolist()
        brandlist.sort()
        brandname = st.selectbox('',brandlist)
        brand(brandname)

        brand_count = df_brand.shape
        ywmd = df_brand.loc[df_brand['Price_inEURO']==df_brand['Price_inEURO'].max()]
        #print(ywmd)
        ywmd = ywmd.values.tolist()

        YearCorr()
        Menu1 = ["Year to Year","Month wise","Average distribution per year"]
            
        choice = st.sidebar.selectbox("",Menu1)

        if choice == "Year to Year":

            components.html(f"""
            
            <link href="https://unpkg.com/tailwindcss@^1.0/dist/tailwind.min.css" rel="stylesheet">
            
            <div class="flex rounded-lg shadow-md overflow-hidden mt-4 px-4 py-4">
                <div class="flex flex-wrap gap-x-2  gap-y-2">
    
                    <div class="rounded-lg border-2 border-blue-400 overflow-hidden shadow-md">
                        <div class="px-6 pt-2">
                            <div class="text-l text-blue-400 text-center"><span>Total Count</span></div>
                        </div>
                        <div class="px-6 font-bold text-xl text-blue-500 pb-2"><span>{brand_count[0]}</span></div>
                    </div>
    
                    <div class="rounded-lg overflow-hidden border-2 border-blue-400 shadow-md">
                        <div class="px-6 pt-2">
                            <div class="text-l text-blue-400 text-center"><span>Price Range</span></div>
                        </div>
                        <div class="px-6 font-bold text-blue-500 text-xl pb-2"><span>{df_brand['Price_inEURO'].min()} € - 
                            {df_brand['Price_inEURO'].max()} €</span></div>
                    </div>

                    <div class="rounded-lg overflow-hidden border-2 border-blue-400 shadow-md">
                        <div class="px-6 pt-2">
                            <div class="text-l text-blue-400 text-center"><span>Correlation</span></div>
                        </div>
                        <div class="px-6 font-bold text-xl text-blue-500 pb-2"><span>{"{:.3f}".format(year_price_corr)}</span></div>
                    </div>

                    <div class="overflow-hidden px-6 pt-2">
                        <div >
                            <div class="text-l text-blue-400"><span>Max distribution(Year)</span></div>
                        </div>
                        <div class="font-bold text-gray-500 text-xl pb-2"><span>{ywmd[0][3]}</span></div>
                    </div>

                    <div class="overflow-hidden">
                        <div class="px-2 pt-2">
                            <div class="text-l text-blue-400"><span>Model name</span></div>
                        </div>
                        <div class="px-2 font-bold text-gray-500 text-xl pb-2"><span>{ywmd[0][2]}</span></div>
                    </div>

                    <div class="overflow-hidden">
                        <div class="px-2 pt-2">
                            <div class="text-l text-blue-400"><span>Km driven</span></div>
                        </div>
                        <div class="px-2 font-bold text-gray-500 text-xl pb-2"><span>{ywmd[0][5]}</span></div>
                    </div>
                    
                    <div class="overflow-hidden">
                        <div class="px-2 pt-2">
                            <div class="text-l text-blue-400"><span>Current price</span></div>
                        </div>
                        <div class="px-2 font-bold text-gray-500 text-xl pb-2"><span>{ywmd[0][6]} €</span></div>
                    </div>
                </div>
            </div>""",height=130)

            year_of_registration = df_brand["Year_Of_Registration"]
            price = df_brand['Price_inEURO']
            scatterPlot(year_of_registration, price)

        elif choice == "Month wise":
            st.subheader('Year')
            yearlist = df_brand['Year_Of_Registration'].unique().tolist()
            yearlist.sort()
            Reg_year = st.selectbox("",yearlist)
            
            month_wise(brandname, Reg_year)
            
            monthCorr()

            month_count = df_brand_year.shape

            mwmd = df_brand_year.loc[df_brand_year['Price_inEURO']==df_brand_year['Price_inEURO'].max()]
            mwmd = mwmd.values.tolist()

            components.html(f"""
                <link href="https://unpkg.com/tailwindcss@^1.0/dist/tailwind.min.css" rel="stylesheet">
                <div class="flex rounded-lg shadow-md overflow-hidden mt-4 px-4 py-4">
                    <div class="flex flex-wrap gap-x-2  gap-y-2">
    
                        <div class="rounded-md border-2 border-blue-400 overflow-hidden shadow-lg">
                            <div class="px-6 pt-2">
                            <div class="text-l text-blue-400 text-center"><span>Total Count</span></div>
                        </div>
                        <div class="px-6 font-bold text-xl text-blue-500 pb-2"><span>{month_count[0]}</span></div>
                    </div>
    
                    <div class="rounded-md border-2 border-blue-400 overflow-hidden shadow-lg">
                        <div class="px-6 pt-2">
                            <div class="text-l text-blue-400 text-center"><span>Price Range</span></div>
                        </div>
                        <div class="px-6 font-bold text-blue-500 text-xl pb-2"><span>{df_brand_year['Price_inEURO'].min()} € - 
                            {df_brand_year['Price_inEURO'].max()} €</span></div>
                    </div>

                    <div class="rounded-md  border-2 border-blue-400 overflow-hidden shadow-lg">
                        <div class="px-6 pt-2">
                            <div class="text-l text-blue-400 text-center"><span>Correlation</span></div>
                        </div>
                        <div class="px-6 font-bold text-blue-500 text-xl pb-2"><span>{"{:.3f}".format(month_price_corr)}</span></div>
                    </div>

                    <div class="overflow-hidden px-4 pt-2">
                        <div >
                            <div class="text-l text-blue-400"><span>Max Distribution(Month)</span></div>
                        </div>
                        <div class="font-bold text-gray-500 text-xl pb-2"><span>{mwmd[0][4]}</span></div>
                    </div>

                    <div class="overflow-hidden">
                        <div class="px-2 pt-2">
                            <div class="text-l text-blue-400"><span>Model name</span></div>
                        </div>
                        <div class="px-2 font-bold text-gray-500 text-xl pb-2"><span>{mwmd[0][2]}</span></div>
                    </div>

                    <div class="overflow-hidden">
                        <div class="px-2 pt-2">
                            <div class="text-l text-blue-400"><span>Km driven</span></div>
                        </div>
                        <div class="px-2 font-bold text-gray-500 text-xl pb-2"><span>{mwmd[0][5]}</span></div>
                    </div>
                
                    <div class="overflow-hidden">
                        <div class="px-2 pt-2">
                            <div class="text-l text-blue-400"><span>Current price</span></div>
                        </div>
                        <div class="px-2 font-bold text-gray-500 text-xl pb-2"><span>{mwmd[0][6]} €</span></div>
                    </div>
                </div>
            </div>""",height=130)

            month_of_registration = df_brand_year["Month_Of_Registration"]
            price = df_brand_year['Price_inEURO']
            scatterPlot(month_of_registration, price)
            

        elif choice == "Average distribution per year":
            
            years = df['Year_Of_Registration'].unique()
            
            avg_price = []
            
            for year in years:
                df_year = df_brand.query('Year_Of_Registration == '+str(year))
                avg = np.average(df_year['Price_inEURO'])
                avg_price.append(avg)

            data = {'Years':years, 'Average Price':avg_price}
            avg_df = pd.DataFrame(data)
            avg_df.sort_values(by='Years',inplace=True)

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=avg_df['Years'], y=avg_df['Average Price'],
                    mode='lines+markers',
                    name='lines+markers',
                    marker = dict(size=10,color='white'),
                    line = dict(width=5, color='#636EFA'))),
            fig.update_layout(
                xaxis_title ='Year of registration',
                yaxis_title ='Average Price',
                width = 1100,
                height = 700,
                paper_bgcolor='rgb(40,44,53)',
                plot_bgcolor='rgb(40,44,53)',
                font_color="#636EFA",
                font_size=15
            )
            st.plotly_chart(fig)

            components.html(f"""
                <link href="https://unpkg.com/tailwindcss@^1.0/dist/tailwind.min.css" rel="stylesheet">
                <div class="flex justify-center">    
                    <div class="rounded-lg shadow-md overflow-hidden rounded-md px-4 py-4">
                        
                        <div class="flex flex-wrap gap-x-2  gap-y-2">    
                            
                            <div class="rounded-md overflow-hidden shadow-md">
                                <div class="px-6 pt-2">
                                    <div class="text-l text-blue-400 text-center"><span>Min Average</span></div>
                                </div>
                                <div class="px-6 font-bold text-gray-400 text-xl pb-2">
                                    <span>{"{:.2f}".format(avg_df['Average Price'].min())}</span>
                                </div>
                            </div>
    
                        <div class="rounded-md overflow-hidden shadow-md">
                            
                            <div class="px-6 pt-2">
                                <div class="text-l text-blue-400 text-center"><span>Max Average</span></div>
                            </div>
                            <div class="px-6 font-bold text-gray-400 text-xl pb-2"><span>{"{:.2f}".format(avg_df['Average Price'].max())}
                            </span></div>
                        </div>
                    </div>
                </div>
            </div>""",height=110)

    else:
        st.subheader('Upload data file!!')

if __name__=="__main__":
    write()



    