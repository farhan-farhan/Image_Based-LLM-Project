from dotenv import load_dotenv
import os
load_dotenv()
import streamlit as st
import pathlib
import textwrap
from PIL import Image

import google.generativeai as genai 


os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(input,image,prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input,image[0],prompt])
    return response.text


def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,  
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


input_prompt="""
               Write a creative and engaging story inspired by the following image. Describe the setting, characters, and events in detail. 
               The story should capture the essence and mood of the image, incorporating any visible elements or emotions conveyed. 
               Include dialogue and inner thoughts where appropriate to bring the characters to life. Ensure the story has a clear beginning, middle, and end.
               """


st.set_page_config(page_title="Gemini Image demo")
st.header("Gemini Image Based Applications")
input=st.text_input("Input Prompt: ",key="input")


uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""
if uploaded_file is not None :
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)



submit=st.button("explain the image to me 👇 ")
if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_response(input_prompt,image_data,input)
    st.subheader("The Response is")
    st.write(response)



