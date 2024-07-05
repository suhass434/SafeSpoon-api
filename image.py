import gradio as gr
import pandas as pd
import cv2
import easyocr
import google.generativeai as genai

reader= easyocr.Reader(['en'])
API_KEY = 'AIzaSyC85O_R-H8VhRpxAEj7iUAw0o7NCNJ_VmE'
genai.configure(api_key = API_KEY)

def ocr_genai(image,allergies,age,gender,weight,diseases):
    results=reader.readtext(image)
    results=pd.DataFrame(results,columns=['bbox','text','conf'])
    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat(history = [])
    instruction = ""
    question = ' '.join(results.text)
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

    # Construct the query
    query = (
        f"The ingredients are extracted from EasyOCR and may not be well formatted. "
        f"Extract only the ingredients. {additional_info}"
        f"For each ingredient, determine if it poses a risk to the user. "
        f"If it does, classify the risk level as 'High', 'Moderate', or 'Low', and provide a one-line description explaining why and how it poses a risk. "
        f"The 'risk' field should contain both the risk level and the description. "
        f"The response should be a well-formatted point wise report with the ingredient as the heading, followed by the risk classification and description. "
        f"Finally you should tell me whether the food is safe to eat or not.Please ensure the response is strictly based on ingredients typically found on food labels."
    )
    response = chat.send_message(question+query)

    return response.text

title = "SafeSpoon"
description = "Upload an image of ingredients"
#inputs = gr.Image()
inputs = [
    gr.Image(label="Upload Image"),
    
    gr.Textbox(label="Allergies (comma-separated)", placeholder="e.g., peanuts, dairy, gluten"),
    gr.Textbox(label="age"),
    gr.Textbox(label="gender"),
    gr.Textbox(label="weight"),
    gr.Textbox(label="diseases")
]
outputs = gr.Textbox(label='Results',lines = 20)
interface = gr.Interface(fn=ocr_genai, inputs=inputs, outputs=outputs,title=title)
interface.launch(share=True)
