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
from pandas_profiling import  ProfileReport
from streamlit_pandas_profiling import st_profile_report


@st.cache
def carData(data):

    df = pd.read_csv(data,engine="python")
    df= df.set_index('srno')
    return df

def write():
    
    data = st.sidebar.file_uploader('upload car data file', type='csv')
    st.title('DataSet Summary')
    if data is not None:
        profile = ProfileReport(carData(data))
        st_profile_report(profile)     
    else:
        st.header('Please upload your data file')

if __name__=="__main__":
    write()
