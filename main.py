import os
import streamlit as st
import openai
from datetime import datetime

# Constants
VALID_DATE_FORMAT = "%Y-%m-%d"

@st.cache
def get_api_key():
    api_key = os.getenv('OPENAI_KEY')
    if not api_key:
        st.warning("Please set your OpenAI API Key as an environment variable.")
    return api_key

def validate_input(activity, date, time, importance):
    errors = []
    try:
        datetime.strptime(date, VALID_DATE_FORMAT)
    except ValueError:
        errors.append(f"Unable to parse date: {date}. Please use format YYYY-MM-DD.")
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

@st.cache
def generate_schedule(activities, api_key):
    inputs = "\n".join(", ".join(map(str, activity)) for activity in activities)
    prompt = f"Given the following activities with deadlines, estimated time, and importance:\n{inputs}\nOutput a structured schedule and priority list."
    try:
        openai.api_key = api_key
        response = openai.Completion.create(engine="text-davinci-002", prompt=prompt, max_tokens=150, temperature=0.5)
        return response.choices[0].text.strip(), None
    except openai.error.OpenAIError as e:
        return None, str(e)

def main():
    st.title("ADD/ADHD Project Manager App")
    st.markdown("Welcome! This app will help you organize your tasks and activities.")
    
    st.markdown("Please enter your activity details below:")

    activity = st.text_input("Activity Name")
    date = st.date_input("Deadline")
    time = st.number_input("Estimated Time (in hours)", min_value=0.0, step=0.5)
    importance = st.slider("Importance (a number between 1 to 5)", min_value=1, max_value=5)

    api_key = get_api_key()

    activities = st.session_state.get("activities", [])

    if st.button("Add Activity"):
        is_valid, errors = validate_input(activity, date.strftime(VALID_DATE_FORMAT), time, importance)
        if is_valid:
            activities.append((activity, date.strftime(VALID_DATE_FORMAT), time, importance))
            st.session_state.activities = activities
            st.success("Activity added successfully!")
        else:
            for error in errors:
                st.error(f"Input validation error: {error}")

    if st.button("Generate Schedule"):
        if not api_key:
            st.error("No OpenAI API Key found. Please set your OpenAI API Key as an environment variable.")
        elif not activities:
            st.warning("No activities added yet. Please add some activities first.")
        else:
            schedule, error = generate_schedule(activities, api_key)
            if schedule:
                st.success("Here's your structured schedule:")
                st.write(schedule)
            else:
                st.error(f"An error occurred: {error}")

if __name__ == "__main__":
    main()