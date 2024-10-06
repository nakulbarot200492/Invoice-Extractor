from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

import streamlit as st
import os
import pathlib
import textwrap
from PIL import Image


import google.generativeai as genai

os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(input, image,prompt):
    model=genai.GenerativeModel("gemini-1.5-flash")
    response=model.generate_content([input, image[0],prompt])
    return response.text


def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        bytes_data=uploaded_file.getvalue()

        image_part=[{
            "mime_type" : uploaded_file.type, # Get the mime type of the uploaded file
            "data" : bytes_data
        }]

        return image_part

    else:
        raise FileNotFoundError("No file uploaded")
    




st.set_page_config(page_title="🔍  | Invoice Extractor! 💬")

st.header("Gemini Application")

input=st.text_input("Input Prompt: ", key="input")
uploaded_file=st.file_uploader("Choose an image...", type=['jpeg','jpg', 'png'])
image=""
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)


submit=st.button("Tell me about the image")

prompt="""
        You are an expert in understanding invoices.
        You will receive input images as invoices &
        You will have to answer questions based on the input image
"""

if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_response(prompt,image_data, input)
    st.subheader("The resonse is....")
    st.write(response)


# Add simple footer
st.write("----")
st.write("🧑 Created by: Nakul Barot")





