import streamlit as st
import requests
import json
import base64
from config import API_KEY

st.set_page_config(page_title="Movie Recommendation",page_icon="cinema.png",layout="centered",initial_sidebar_state="auto",menu_items=None)
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html=True)

st.markdown("""
    ## Movie Recommendation System"""
    ,
    unsafe_allow_html=True)

def add_bg(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )

def hideAll():
    hide = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """   
    st.markdown(hide,unsafe_allow_html=True)

def remove_underline():
    st.markdown(
        """
        <style>
        a {
            text-decoration: none;
            color : black;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg('Bg-image.png') 
def movie(movieName):
    colm_1,colm_2 = st.columns(2)
    try:
        url = "https://online-movie-database.p.rapidapi.com/auto-complete"
        querystring = {f"q":{movieName}}
        headers = {
            "X-RapidAPI-Key": API_KEY,
            "X-RapidAPI-Host": "online-movie-database.p.rapidapi.com"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        datas = json.loads(response.text)
        remove_underline()
        try:
            index = 0
            for index, new_element in enumerate(datas['d']):
                if index % 2 == 0:
                    column = colm_1
                else:
                    column = colm_2
            
                with column:
                    st.markdown('<div id="movie-title">Title of the Movie</div>'
                        ,
                        unsafe_allow_html=True)
                    st.write(str(new_element['l']))

                    st.image(new_element.get('i', {}).get('imageUrl'), width=300)
            
                    st.write(f"Cast : {str(new_element['s'])}")
                    st.write(f"Year of release : {str(new_element['y'])}")
                    name = str(new_element['l'])
                    name = name.replace(" ", "+")
                    name = name.replace(":", "")
                    year = str(new_element['y'])
                    st.markdown(f"[For more info...](https://www.google.com/search?q={name}+{year})", unsafe_allow_html=True)
        except:
            pass
    except:
        st.write("Got an Error")

def top():
    colm_1,colm_2 = st.columns(2)
    try:
        url = "https://imdb-top-100-movies.p.rapidapi.com/"
    
        headers = {
            "X-RapidAPI-Key": "132d97dc1emsh74614bee7028c43p1ce01bjsna30851e6698e",
            "X-RapidAPI-Host": "imdb-top-100-movies.p.rapidapi.com"
        }
            
        response = requests.get(url, headers=headers)
        datas = json.loads(response.text)
        # print(datas)
        remove_underline()
        try:
            index = 0
            for index, new_element in enumerate(datas):
                if index % 2 == 0:
                    column = colm_1
                else:
                    column = colm_2
            
                with column:
                    st.markdown('<div id="movie-title">Title of the Movie</div>'
                        ,
                        unsafe_allow_html=True)
                    st.write(new_element['title'])
                    st.image(new_element['image'], width=300)
                    st.write("Year of release : ",str(new_element['year']))
                    name = str(new_element['title'])
                    name = name.replace(" ", "+")
                    name = name.replace(":", "")
                    year = str(new_element['year'])
                    st.markdown(f"[For more info...](https://www.google.com/search?q={name}+{year})", unsafe_allow_html=True)
                    st.write("---")
        except:
            pass
    except:
        st.write("Got an Error")

hideAll()
movieName = st.text_input("Enter the name of Movie to recommend : ")
if movieName == '':
    st.header("Top Movies for You!")
    top()
else:
    movie(movieName)
    st.markdown("""
    ## Thanks for using our Services
    """)
