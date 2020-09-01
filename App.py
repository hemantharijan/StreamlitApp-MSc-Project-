import streamlit as st

import awesome_streamlit as ast
import pages.Sentiment
import pages.WordFreq
import pages.DataSummary
import pages.PriceDistribution

import streamlit.components.v1 as components

ast.core.services.other.set_logging_format()

st.set_option('deprecation.showfileUploaderEncoding', False)

#CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
#local_css("style.css")

#Hiding footer
hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            fullscress {visibility:hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 


Menu1 = {
    "Sentiment Analysis":pages.Sentiment,
    "Word Frequency":pages.WordFreq,
    "Upload Car Data": pages.DataSummary,
    "Price Distribution": pages.PriceDistribution
}


def main():
    st.sidebar.title("Menu")   
    selection = st.sidebar.radio("Go to",list(Menu1.keys()))
    
    st.sidebar.markdown(
           """<head><style>
                .color{ 
                    color:blue;
                    background-color:blue;
                    height:3px;
                    widht:50px;}</style></head>
                <div class="color"></div>""", unsafe_allow_html=True)
    
    page = Menu1[selection]
    if selection is not False:
        with st.spinner(f"Loading Data..."):
            ast.shared.components.write_page(page)
            print(selection)
            st.sidebar.markdown(
                """<head><style>
                    .color{
                        color:blue;
                        background-color:blue;
                        height:3px;
                        widht:50px;}</style></head>
                    <div class="color"></div>""", unsafe_allow_html=True)
    
if __name__=="__main__":
    main()





