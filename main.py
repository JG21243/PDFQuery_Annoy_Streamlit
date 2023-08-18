import os
import streamlit as st
import openai
from datetime import datetime
from streamlit_calendar import Calendar

# Constants
VALID_DATE_FORMAT = "%Y-%m-%d"

def validate_input(activity, date, time, importance):
    errors = []
    if not activity:
        errors.append("Activity name cannot be empty.")
    try:
        float(time)
    except ValueError:
        errors.append(f"Unable to parse estimated time: {time}. Please input a number.")
    try:
        importance = int(importance)
        if importance < 1 or importance > 5:
            errors.append(f"Importance should be a number between 1 and 5: {importance}")
    except ValueError:
        errors.append(f"Unable to parse importance: {importance}. Please input a number.")
    return not errors, errors

def generate_schedule(activities, api_key):
    openai.api_key = api_key

    # Prepare the input for GPT-3.5-turbo
    input_text = "Generate a schedule for the following activities, prioritizing tasks based on their importance and deadline:\n"
    for act in activities:
        formatted_date = act[1].strftime(VALID_DATE_FORMAT)
        input_text += f"{act[0]} - Deadline: {formatted_date} - Time: {act[2]} hours - Importance: {act[3]}\n"

    # Call the GPT-3.5-turbo API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": input_text
            }
        ],
        max_tokens=1500,
        n=1,
        stop=None,
        temperature=0.1,
    )

    # Extract the generated schedule
    schedule = response.choices[0].message['content'].strip()

    return schedule, None

def main():
    st.title("Project Manager App")
    st.markdown("Welcome! This app will help you organize your tasks and activities.")
    
    st.markdown("Please enter your activity details below:")

    activity = st.text_input("Activity Name")
    date = st.date_input("Deadline")
    time = st.number_input("Estimated Time (in hours)", min_value=0.0, step=0.5)
    importance = st.slider("Importance (a number between 1 to 5)", min_value=1, max_value=5)

    api_key = st.sidebar.text_input("OpenAI API Key", type="password")

    activities = st.session_state.get("activities", [])

    if st.button("Add Activity"):
        is_valid, errors = validate_input(activity, date, time, importance)
        if is_valid:
            activities.append((activity, date, time, importance))
            st.session_state.activities = activities
            st.success("Activity added successfully!")
        else:
            for error in errors:
                st.error(f"Input validation error: {error}")

    if st.button("Generate Schedule"):
        if not api_key:
            st.error("No OpenAI API Key found. Please enter your OpenAI API Key in the sidebar.")
        elif not activities:
            st.warning("No activities added yet. Please add some activities first.")
        else:
            schedule, error = generate_schedule(activities, api_key)
            if schedule:
                st.success("Here's your structured schedule:")

                # Format the schedule output
                schedule_lines = schedule.split('\n')
                events = []
                for line in schedule_lines:
                    # Parse the schedule line to extract the event information
                    # You may need to adjust the parsing logic based on the format of your schedule
                    event_name, event_date = line.split(" - ")[0], line.split(" - ")[1]
                    events.append({"title": event_name, "start": event_date})

                # Display the calendar with the events
                st.write(Calendar(events=events, view="dayGridMonth", theme="light"))

            else:
                st.error(f"An error occurred: {error}")

if __name__ == "__main__":
    main()
