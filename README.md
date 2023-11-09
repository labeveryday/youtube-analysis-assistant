# YouTube Analysis Assistant

Welcome to the YouTube Analysis Assistant, a tool designed to help you optimize and enhance your YouTube content using the power of language models. This assistant can suggest engaging titles, SEO tags, thumbnail designs, content enhancements, and segments with viral potential for your YouTube videos.

![Screen copy](./img/screencopy.gif)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install the software and how to install them:

- Python 3.6+
- Pip (Python package installer)
- Virtual environment (optional but recommended)

### Installation

A step-by-step series of examples that tell you how to get a development environment running:

1. **Clone the repository**
    ```sh
    git clone https://github.com/labeveryday/youtube-analysis-assistant.git
    ```
2. **Navigate to the project directory**
    ```sh
    cd youtube-analysis-assistant
    ```

3. **Set up a Python virtual environment (Optional but recommended)**
    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

4. **Install the required packages**
    ```sh
    pip install -r requirements.txt
    ```

5. **Set up the `.env` file**
    - Copy the `.env.example` to a new file named `.env`
    - Add your OpenAI API key to the `.env` file:
        ```
        OPENAI_API_KEY='your_openai_api_key_here'
        ```

6. **Run the Streamlit application**
    ```sh
    streamlit run app.py
    ```

### Usage

Once the application is running, you can interact with it through the Streamlit UI in your web browser.

1. **Insert the YouTube URL** you wish to analyze in the sidebar input.
2. **Click Submit** to process the video through the YouTube Loader.
3. **Interact with the analysis assistant** by typing in your questions or commands.

### Features

- Video transcript fetching and processing
- Conversation with LLM for content suggestions
- UI components for a user-friendly experience
- Transcript download functionality

### File Descriptions

- `app.py`: The main application script that contains the Streamlit UI and logic.
- `requirements.txt`: A list of necessary Python packages.
- `.env`: A file for storing environmental variables (OPENAI_API_KEY not included, you must [create your own](https://platform.openai.com)).


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

### About me

My passions lie in Network Engineering, Cloud Computing, Automation, and impacting people's lives. I'm fortunate to weave all these elements together in my role as a Developer Advocate. On GitHub, I share my ongoing learning journey and the projects I'm building. Don't hesitate to reach out for a friendly hello or to ask any questions!

My hangouts:
- [LinkedIn](https://www.linkedin.com/in/duanlightfoot/)
- [YouTube](https://www.youtube.com/@LabEveryday)