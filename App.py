import nltk
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.figure_factory as ff

from io import StringIO, BytesIO
from numpy import cov
from textblob import TextBlob
from collections import Counter
from scipy.stats import pearsonr
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

import awesome_streamlit as ast
import pages.Sentiment
import pages.WordFreq
ast.core.services.other.set_logging_format()



st.set_option('deprecation.showfileUploaderEncoding', False)



#CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
local_css("style.css")

#Hiding footer
hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 


PAGES = {
    "Sentiment Analysis":pages.Sentiment,
    "Word Frequency":pages.WordFreq
}

def main():
    st.sidebar.title("Menu")
    selection = st.sidebar.radio("Go to",list(PAGES.keys()))

    page = PAGES[selection]
    with st.spinner(f"Loading Data..."):
        ast.shared.components.write_page(page)

if __name__=="__main__":
    main()





