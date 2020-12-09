import streamlit as st
import awesome_streamlit as ast
import pages.Sentiment
import pages.WordFreq
import pages.DataSummary
import pages.PriceDistribution
import pages.kmDistribution
import pages.price_predictor
import pages.CarBrands
import pages.Models
import pages.Features

st.set_option('deprecation.showfileUploaderEncoding', False)

#CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}',
         unsafe_allow_html=True)
local_css("style.css")

st.markdown(
        f"""<style>
        .reportview-container .main .block-container{{
            max-width: 2000px;
            padding-top: 0rem;
            padding-right: 4rem;
            padding-left: 4rem;
            padding-bottom: 0rem;}}
        </style>""", unsafe_allow_html=True,)



#Hiding footer
hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            fullscreen {visibility:hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

Menu1 = {
    "Sentiment Analysis":pages.Sentiment,
    "Word Frequency":pages.WordFreq,
    "Data Summary": pages.DataSummary,
    "Price Distribution": pages.PriceDistribution,
    "Km Distribution": pages.kmDistribution,
    "Brands": pages.CarBrands,
    "Models" : pages.Models,
    "Features" : pages.Features,
    "Price Predictor": pages.price_predictor,
     }

def main():
    
    st.sidebar.title("Menu")
    selection = st.sidebar.radio("",list(Menu1.keys()))
    page = Menu1[selection]
    if selection is not False:
        with st.spinner(f"Loading Data..."):
            st.write(
        """
        <style type="text/css" media="screen">
        div[role="listbox"] ul {
            height:300px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

            st.sidebar.title(selection)
            ast.shared.components.write_page(page)

if __name__=="__main__":
    main()





