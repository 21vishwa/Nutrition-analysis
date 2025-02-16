import google.generativeai as genai
from googletrans import Translator

genai.configure(api_key="AIzaSyAInDBdmePXN7ps16dHrh01t9HL8L6I_9E")
translator = Translator()


def get_gemini_response(input_prompt, image):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([input_prompt, image[0]])
        return response.text
    except Exception as e:
        return f"Error from Gemini model: {e}"

def translate_text(text, lang):
    return translator.translate(text, dest=lang).text