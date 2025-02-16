from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import mysql.connector
from mysql.connector import Error
import pandas as pd
from datetime import datetime
import calendar  # Import the calendar module
from db_operations import insert_user, verify_user, insert_meal, get_meals_for_user, user_exists
from external_services import get_gemini_response, translate_text
from image_processing import input_image_setup
from utility_functions import translate_ui_elements, set_upload_mode, set_capture_mode, reset_mode
from handlers.login_signup import handle_login_signup
from handlers.image_handler import handle_image_input
from handlers.meal_analysis import display_meal_analysis
from handlers.meal_calendar import display_calendar

# Load environment variables
load_dotenv()

# Initialize Streamlit App
st.set_page_config(page_title="The Nutritionist", layout="centered")

# Initialize session state for mode
if 'mode' not in st.session_state:
    st.session_state['mode'] = None

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# Initialize session state for year and month selection
if 'selected_year' not in st.session_state:
    st.session_state['selected_year'] = datetime.now().year
if 'selected_month' not in st.session_state:
    st.session_state['selected_month'] = datetime.now().strftime('%B')  # Store as string for month name

if not st.session_state['logged_in']:
    st.subheader("Login / Signup")
    handle_login_signup()
else:
    # Language Selection
    language = st.selectbox("Select Language", ["English", "Hindi", "Tamil", "Telugu"])
    lang_map = {
        "English": "en",
        "Hindi": "hi",
        "Tamil": "ta",
        "Telugu": "te"
    }

    translations = translate_ui_elements(lang_map[language])

    # Set page title
    st.title(translations["title"])

    # User inputs for meal tracking
    user_name = st.text_input(translations["name_input"])
    meal_date = st.date_input(translations["date_input"])
    meal_time = st.time_input(translations["time_input"])

    # Display buttons
    col1, col2 = st.columns(2)
    with col1:
        upload_button = st.button(translations["upload_button"], on_click=set_upload_mode)
    with col2:
        capture_button = st.button(translations["capture_button"], on_click=set_capture_mode)

    st.markdown("---")

    # Handle image inputs
    handle_image_input(translations, st.session_state['mode'], user_name, meal_date, meal_time, lang_map, language)

    # Display meals for user on the selected date
    display_meal_analysis(user_name, meal_date, translations, lang_map, language)
    
    # Calendar Year and Month Selection
    st.subheader("Food Diary Calendar")
    st.session_state['selected_year'] = st.number_input("Select Year", value=st.session_state['selected_year'], min_value=1900, max_value=2100)

    month_names = list(calendar.month_name)[1:]  # January to December

    # Use the index of the selected month for the selectbox
    current_month_index = month_names.index(st.session_state['selected_month'])

    # Update the selectbox to manage it properly as an index
    st.session_state['selected_month'] = st.selectbox("Select Month", month_names, index=current_month_index)

    # Show the calendar with selected year and month
    if st.button("Show Food Diary Calendar"):  # Add this button to trigger calendar display
        display_calendar(user_name, st.session_state['selected_year'], month_names.index(st.session_state['selected_month']) + 1)

    # Reset mode button
    st.button(translations["reset_button"], on_click=reset_mode)

    # Display the nutritional analysis if a meal was selected
    if 'selected_meal_analysis' in st.session_state:
        meal_type, meal_time, analysis = st.session_state['selected_meal_analysis']
        st.markdown(f"### Nutritional Analysis for {meal_type} at {meal_time.strftime('%H:%M')}:")
        st.write(analysis)

        # Clear the selection after displaying the analysis
        if st.button("Clear Selection"):
            del st.session_state['selected_meal_analysis']
