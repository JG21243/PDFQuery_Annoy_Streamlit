
# ADD/ADHD Project Manager App

This is a Streamlit application that uses OpenAI's GPT-3 to generate a schedule and prioritize tasks for individuals with ADD/ADHD.

## Getting Started

These instructions will help you set up the project on your local machine for development and testing purposes.

### Prerequisites

Below are the software requirements to get your project up and running:

1. Python 3.11 (you can download it from [here](https://www.python.org/downloads/))
2. Streamlit 1.3.0
3. OpenAI 0.27.0

### Installing

Here are the steps to install the required Python packages using pip:

```bash
pip install streamlit==1.3.0
pip install openai==0.27.0
```

You also need to set the `OPENAI_KEY` environment variable to your OpenAI API key. This key is required to use the OpenAI GPT-3 API.

### Running the Application

You can run your Streamlit application using the following command:

```bash
streamlit run app.py
```

Replace `app.py` with the name of your Python script.

## Application Overview

The application allows the user to input tasks with their estimated time to completion, deadline, and importance. The OpenAI GPT-3 engine is then used to generate a structured schedule and task priority list.

## Authors

List the main authors or contributors here.

## License

This project is licensed under the MIT License.

## Acknowledgments

You can add some acknowledgments here (if applicable).
