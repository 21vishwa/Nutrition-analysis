import streamlit as st
import pandas as pd
from external_services import translate_text
from db_operations import get_meals_for_user
from datetime import datetime

def display_meal_analysis(user_name, meal_date, translations, lang_map, language):
    """ Display meals consumed by user on selected date """
    if st.button(translations["show_analysis"]):
        meals = get_meals_for_user(user_name, meal_date)
        if meals:
            st.write("### Meals Consumed on ", meal_date)
            meal_data = []
            for meal_time, analysis in meals:
                meal_time_formatted = (datetime.min + meal_time).time()
                translated_analysis = translate_text(analysis, lang_map[language])
                meal_data.append({"Time": meal_time_formatted, "Analysis": translated_analysis})

            meal_df = pd.DataFrame(meal_data)
            st.table(meal_df)
        else:
            st.write("No meals recorded for this date.")
