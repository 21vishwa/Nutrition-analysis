import streamlit as st
from PIL import Image
from external_services import get_gemini_response, translate_text
from image_processing import input_image_setup
from db_operations import insert_meal
with open('prompts/prompt_upload.txt', 'r') as file:
    input_prompt_upload = file.read()

def handle_image_input(translations, mode, user_name, meal_date, meal_time, lang_map, language):
    """ Handle image uploads and captures """
    if mode == 'upload':
        st.subheader(translations["upload_subheader"])
        uploaded_file = st.file_uploader(translations["image_uploader"], type=["jpg", "jpeg", "png"])

        if uploaded_file is not None:
            process_uploaded_image(uploaded_file, translations, user_name, meal_date, meal_time, lang_map, language)

    elif mode == 'capture':
        st.subheader(translations["capture_subheader"])
        camera_input = st.camera_input("📸 Take a picture")

        if camera_input is not None:
            process_captured_image(camera_input, translations, user_name, meal_date, meal_time, lang_map, language)

def process_uploaded_image(uploaded_file, translations, user_name, meal_date, meal_time, lang_map, language):
    try:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image.", use_column_width=True)

        submit = st.button(translations["analyze_button"])

        if submit:
            with st.spinner("Analyzing..."):
                image_parts = input_image_setup(uploaded_file)
                response = get_gemini_response(input_prompt_upload,image_parts)
                st.markdown(translations["nutrition_analysis"])
                translated_response = translate_text(response, lang_map[language])
                st.write(translated_response)
                insert_meal(user_name, meal_date, meal_time, response)

    except Exception as e:
        st.error(f"An error occurred: {e}")

def process_captured_image(camera_input, translations, user_name, meal_date, meal_time, lang_map, language):
    try:
        image = Image.open(camera_input)
        st.image(image, caption="Captured Image.", use_column_width=True)

        submit = st.button(translations["analyze_button"])

        if submit:
            with st.spinner("Analyzing the image..."):
                image_data = input_image_setup(camera_input)
                response = get_gemini_response(input_prompt_upload, image_data)
                translated_response = translate_text(response, lang_map[language])
                st.markdown(translations["nutrition_analysis"])
                st.write(translated_response)
                insert_meal(user_name, meal_date, meal_time, response)

    except Exception as e:
        st.error(f"An error occurred: {e}")
