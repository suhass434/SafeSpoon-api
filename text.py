import gradio as gr
import pandas as pd
import cv2
import easyocr
import google.generativeai as genai

reader= easyocr.Reader(['en'])
API_KEY = 'AIzaSyC85O_R-H8VhRpxAEj7iUAw0o7NCNJ_VmE'
genai.configure(api_key = API_KEY)



def ocr_genai(text,allergies,age,gender,weight,diseases):
    additional_info = ""
    if allergies:
        additional_info += "allergic to {allergies}. "
    if age:
        additional_info += f"User age: {age}. "
    if gender:
        additional_info += f"User gender: {gender}. "
    if weight:
        additional_info += f"User weight: {weight}. "
    if diseases:
        additional_info += f"User diseases: {diseases}. "


    ingredients_text = text
    query = (
    f"The food items provided are: {ingredients_text}.user details {additional_info}"
    f"Extract and identify the ingredients that may be used in it."
    f"For each ingredient, determine if it poses a risk to the user. "
    f"If it does, classify the risk level as 'High', 'Moderate', or 'Low', and provide a one-line description explaining why and how it poses a risk. "
    f"The 'risk' field should contain both the risk level and the description. "
    f"The response should be a well-formatted point wise report with the possible ingredients in the given food item, followed by the risk classification and description. "
    f"Finally you should tell me whether the food is safe to eat or not.Please ensure the response is strictly based on food items.And the whole response should not contain bold letter(or stars in the response)")
    
    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat(history = [])
    instruction = ""
    #question = ' '.join(results.text.astype(str))

    response = chat.send_message(ingredients_text+query)

    return response.text

title = "SafeSpoon"
description = "Upload the food item" 

inputs = [
    gr.Textbox(label="Type Ingredients"),
    gr.Textbox(label="Allergies (comma-separated)", placeholder="e.g., peanuts, dairy, gluten"),
    gr.Textbox(label="age"),
    gr.Textbox(label="gender"),
    gr.Textbox(label="weight"),
    gr.Textbox(label="diseases")
]
outputs = gr.Textbox(label='Results',lines = 20)
interface = gr.Interface(fn=ocr_genai, inputs=inputs, outputs=outputs,title=title)
interface.launch(share=True)
