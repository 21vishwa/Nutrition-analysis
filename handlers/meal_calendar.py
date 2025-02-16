from datetime import datetime as dt, timedelta
import streamlit as st
import calendar
from db_operations import get_meals_for_user

def get_meal_type(meal_time):
    """Determine the type of meal based on the time."""
    if isinstance(meal_time, (dt, dt)):
        meal_time = meal_time.time()
    elif isinstance(meal_time, timedelta):
        # Convert timedelta to time
        meal_time = (dt.min + meal_time).time()

    breakfast_threshold = dt.strptime('10:00', '%H:%M').time()
    lunch_threshold = dt.strptime('16:00', '%H:%M').time()
    dinner_threshold = dt.strptime('20:00', '%H:%M').time()

    if meal_time < breakfast_threshold:
        return 'Breakfast'
    elif meal_time < lunch_threshold:
        return 'Lunch'
    elif meal_time < dinner_threshold:
        return 'Snacks'
    else:
        return 'Dinner'

def display_calendar(user_name, year, month_index):
    st.subheader("Food Diary Calendar")
    
    # Create a calendar for the selected month
    cal = calendar.Calendar()
    month_days = cal.monthdayscalendar(year, month_index)

    # Display the calendar grid
    for week in month_days:
        cols = st.columns(len(week))
        for i, day in enumerate(week):
            if day == 0:
                cols[i].write("")  # Empty space for blank days
            else:
                date_str = f"{year}-{month_index:02}-{day:02}"
                cols[i].write(f"{day}")  # Display day

                meal_entries = get_meals_for_user(user_name, date_str)
                if meal_entries:
                    for j, (meal_time, analysis) in enumerate(meal_entries):
                        # Ensure meal_time is a time object
                        if isinstance(meal_time, dt):
                            meal_time = meal_time.time()
                        elif isinstance(meal_time, timedelta):
                            # Convert timedelta to time
                            meal_time = (dt.min + meal_time).time()

                        meal_type = get_meal_type(meal_time)
                        button_label = f"{meal_type} ({meal_time.strftime('%H:%M')})"

                        # Create a unique key for the button
                        unique_key = f"{date_str}_{meal_time}_{j}"
                        if cols[i].button(button_label, key=unique_key):
                            # Store the selected meal analysis in session state
                            st.session_state['selected_meal_analysis'] = (meal_type, meal_time, analysis)
                            # Optionally, show a success message
                            st.success(f"Selected: {meal_type} at {meal_time.strftime('%H:%M')}")

                else:
                    cols[i].write("No meals recorded.")

    # Display the nutritional analysis if a meal was clicked
    if 'selected_meal_analysis' in st.session_state:
        meal_type, meal_time, analysis = st.session_state['selected_meal_analysis']
        st.markdown(f"### Nutritional Analysis for {meal_type} at {meal_time.strftime('%H:%M')}:")
        st.write(analysis)

        # Clear the selection after displaying the analysis
        if st.button("Clear Selection"):
            del st.session_state['selected_meal_analysis']
