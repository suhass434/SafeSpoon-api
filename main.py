import gradio as gr
import pandas as pd
import cv2
import easyocr
import google.generativeai as genai

reader= easyocr.Reader(['en'])
API_KEY = ''
genai.configure(api_key = API_KEY)

def ocr_genai(image,allergies):
    results=reader.readtext(image)
    results=pd.DataFrame(results,columns=['bbox','text','conf'])
    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat(history = [])
    instruction = ""
    question = ' '.join(results.text.astype(str))
    response = chat.send_message(
    question + f"""The ingredients are extracted from EasyOCR and may not be well formatted. 
    Extract only the ingredients. 
    The user is allergic to {allergies}. 
    For each ingredient, determine if it poses a risk to the user. 
    If it does, classify the risk level as 'High', 'Moderate', or 'Low', and provide a one-line description explaining why and how it poses a risk.
    The 'risk' field should contain both the risk level and the description.
    The response should be a well-formatted report with the ingredient as the heading, followed by the risk classification and description. 
    Please ensure the response is strictly based on ingredients typically found on food labels.""")


    return response.text

title = "SafeSpoon"
description = "Upload an image of ingredients"
#inputs = gr.Image()
inputs = [
    gr.Image(label="Upload Image"),
    
    gr.Textbox(label="Allergies (comma-separated)", placeholder="e.g., peanuts, dairy, gluten")
]
outputs = gr.Textbox(label='Results',lines = 20)
interface = gr.Interface(fn=ocr_genai, inputs=inputs, outputs=outputs,title=title)
interface.launch(share=True)
