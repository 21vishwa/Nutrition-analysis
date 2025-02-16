import streamlit as st
from external_services import translate_text

def translate_ui_elements(language):
    """Translate UI elements based on selected language."""
    elements = {
        "title": "🥗 The Nutritionist",
        "upload_button": "📤 Upload Image",
        "capture_button": "📷 Live Capture",
        "upload_subheader": "Upload an Image for Nutrition Analysis",
        "capture_subheader": "Capture an Image for Nutrition Analysis",
        "image_uploader": "Choose an image...",
        "analyze_button": "🔍 Tell me about the calories",
        "nutrition_analysis": "### 📝 Nutrition Analysis",
        "reset_button": "🔄 Reset",
        "name_input": "👤 Enter your name:",
        "date_input": "📅 Select the date of the meal:",
        "time_input": "⏰ Select the time of the meal:",
        "show_analysis": "Show Nutrient Analysis"
    }
    return {key: translate_text(value, language) for key, value in elements.items()}

def set_upload_mode():
    st.session_state['mode'] = 'upload'

def set_capture_mode():
    st.session_state['mode'] = 'capture'

def reset_mode():
    st.session_state['mode'] = None
