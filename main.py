import os
import streamlit as st
import openai
from datetime import datetime
from streamlit_echarts import st_echarts

# ... (other code)

def main():
    # ... (other code)

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
                calendar_data = [
                    {"value": [event["start"], 1]} for event in events
                ]
                calendar_option = {
                    "visualMap": {
                        "show": False,
                        "min": 0,
                        "max": 1
                    },
                    "calendar": {
                        "range": "2023"
                    },
                    "series": {
                        "type": "heatmap",
                        "coordinateSystem": "calendar",
                        "data": calendar_data
                    }
                }
                st_echarts(options=calendar_option)

            else:
                st.error(f"An error occurred: {error}")

    # ... (other code)

if __name__ == "__main__":
    main()

