import streamlit as st
import awesome_streamlit as ast
import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from pandas_profiling import  ProfileReport
from streamlit_pandas_profiling import st_profile_report


@st.cache
def carData(data):
    df = pd.read_csv(data,engine="python")
    df= df.set_index('srno')
    return df

def write():
    
    data = st.sidebar.file_uploader('upload car data file', type='csv')
    
    components.html(f"""
             <link href="https://unpkg.com/tailwindcss@^1.0/dist/tailwind.min.css" rel="stylesheet">
                <div class="flex">
                    <div class="flex-auto rounded-md shadow-lg overflow-hidden text-gray-400 font-bold 
                    rounded-md text-xl border-2 border-blue-500 text-center px-4 py-4 m-2">
                    Data Summary
                    </div>
                </div>
    """,height=90)
    
    if data is not None:
        profile = ProfileReport(carData(data))
        st_profile_report(profile)     
    else:
        st.subheader('Upload data file!!')

if __name__=="__main__":
    write()
