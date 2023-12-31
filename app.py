"""
YouTube Analysis Assistant
"""
import os
import re
from random import randint
from dotenv import load_dotenv

# Used to display the UI components
import streamlit as st
from streamlit_chat import message

import openai
from PIL import Image

# Used to conversation with LLM
from langchain.prompts import PromptTemplate
from langchain.document_loaders import YoutubeLoader
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI

# Load environment variables
load_dotenv()

# Import openai api key
openai.api_key=os.getenv("OPENAI_API_KEY")

# Create title and header
st.set_page_config(page_title="YouTube Analysis", page_icon="🤖", layout="wide")
st.header("YouTube Analysis Assistant 🤖", divider="blue")
st.subheader('I am here to help you improve your :red[YouTube] channel:')


def get_video_transcript(url: str) ->YoutubeLoader:
    """
    Fetches and transcribes the video contents for a given YouTube video ID.

    Args:
        url (str):                          The unique identifier of the YouTube video.

    Returns:
        loaded_video_document (str):        The transcribed contents of the video.
    """
    # The loader downloads and transcribes the video and creates document loader
    loader = YoutubeLoader.from_youtube_url(url, add_video_info=True)
    # Loads the documents
    loaded_video_document = loader.load()
    # Returns the transcribed contents
    return loaded_video_document


def create_prompt(context):
    """
    Generates a prompt from the video transcript.

    Args:
        context (str):      The transcribed contents of the video.

    Returns:
        prompt (str):        The prompt template with the video transcript.
    """
    thumbnail = """Create a vibrant and eye-catching imageg. \
        It should feature a high-contrast color scheme with bright, bold colors. \
        In the center, place a large, intriguing, and slightly exaggerated facial expression of a person looking surprised or excited, \
        ensuring the emotion is highly visible and engaging. Include an element of mystery or curiosity, \
        such as a blurred background image or an object that's partially visible, to spark viewers' interest. \
        Ensure the text color contrasts well with the background for readability. \
        Optionally, add a small, eye-catching icon or emoji in one corner to emphasize the video's theme, like a flame for something 'hot' or a laughing emoji for humor. \
        The overall design should be clean, not too cluttered, but with enough visual elements to stand out and grab attention in a sea of other thumbnails."""
    questions = f"""
    1. Engaging Title: Propose a catchy and appealing title that encapsulates the essence of the content. \
    2. SEO Tags: Identify a list of SEO-friendly tags that are relevant to the content and could improve its searchability. \
    3. Thumbnail Design: {thumbnail} \
    4. Content Enhancement: Offer specific suggestions on how the content could be improved for viewer engagement and retention. \
    5. Viral Potential Segment: Identify the best section that might have the potential to be engaging or entertaining for a short-form viral video based on factors like humor, uniqueness, relatability, or other notable elements. \
    Provide the text section and explain why. \
    6. Create and provide an engaging viral LinkedIn post that would entice viewers to watch the video. \
    7. Create and provide an engaging viral Twitter post that would entice viewers to watch the video. \
    8. Create and provide a summary description of the video that would entice viewers to watch the video. \
    """
    prompt_template = PromptTemplate.from_template("""You are a expert content editor. \
    Your first task is to provide a concise 4-6 sentence 6th grade reading level summary of the given text as if you were preparing an introduction for a personal blog post. \
    Begin your summary with a phrase such as 'In this post' or 'In this interview,' setting the stage for what the reader can expect.
    Your second task is to provide your responses to the following inquiries in the form of bullet points:  \
    
    {context}

    Provide Summary Here: 
    
    Answer Inquiries Here: {questions}
    """
    )
    prompt = prompt_template.format(context=context, questions=questions)
    return prompt

def convert_to_text_file(content):
    """
    Converts the transcript to a text file and returns the file path.

    Args:
        content (str):          The transcribed contents of the video.

    Returns:
        file_path (str):        The file path of the text file.
    """
    # Creates file name in video_id to published date format
    file_name = content[0].metadata["source"] + f"-{content[0].metadata['publish_date'].split(' ')[0]}"
    # Creates a transcript with the title of video as header
    transcript = content[0].metadata["title"] + "\n\n" + content[0].page_content
    file_path = f"./transcripts/{file_name}.txt"
    with open(file_path, 'w') as file:
        file.write(transcript)
    return file_path

def generate_thumbnail(prompt):
    """
    Generates a thumbnail image based on a given prompt using the OpenAI DALL-E 3 model.

    Args:
    prompt (str): A text description of the image to be generated. This prompt is used by the AI model to understand what kind of image is requested.

    Returns:
    str: A URL pointing to the generated image. This URL can be used to view or download the image.
    """
    img_response = openai.images.generate(
        model="dall-e-3",
        prompt = prompt,
        quality="hd",
        n=1,
        #style="natural",
        size="1024x1024")
    image_url = img_response.data[0].url
    return image_url


@st.cache_resource
def load_chain():
    """
    Loads the LLM and the memory.
    
    Returns:
        chain (ConversationChain):      The LLM and the memory.
    """
    llm = ChatOpenAI(
        model_name="gpt-4-1106-preview", 
        openai_api_key=openai.api_key,
        temperature=1,
        verbose=True
    )
    memory = ConversationBufferMemory()
    chain = ConversationChain(llm=llm, memory=memory)
    return chain

# Contains the LLM and the memory
chain = load_chain()

# Creates session state variables
if "generated" not in st.session_state:
    st.session_state["generated"] = []
if "previous" not in st.session_state:
    st.session_state["previous"] = []
if "unique_id" not in st.session_state:
    st.session_state["unique_id"] = str(randint(1000, 10000000))

# Sidebar to clear the chat
st.sidebar.title("Sidebar")
clear_button = st.sidebar.button("Clear Conversation", key="clear")

# This is a hack to clear the chat
if clear_button:
    st.session_state.update({"generated": [], "previous": [], "unique_id": str(randint(1000, 10000000))})
    chain.memory.clear()

# Gets video transcript from url
url = st.sidebar.text_input("Insert YouTube URL", key=st.session_state["unique_id"])
submitted_button = st.sidebar.button("Submit", key=st.session_state["unique_id"] + "submit")      

# Container to display previous conversations
response_container = st.container()
# Container input text box
container = st.container()

# Creates a form with a text area for user input and a submit button.
with container:
    with st.form(key="youtub_app", clear_on_submit=True):
        user_input = st.text_area("You:", key="input", height=100)
        submit_button = st.form_submit_button(label="Send")

    # When submit button clicked and user input is received a prompt is sent to the LLM
    if submit_button and user_input:
        output = chain(user_input)["response"]
        st.session_state["previous"].append(user_input)
        st.session_state["generated"].append(output)
    
    # When user input is received and submit button gets the video transcript from the URL, converts the contents to a text file, and stores the path to the transcript file.
    elif user_input is not None and submitted_button is True:
        contents = get_video_transcript(url)
        transcript_file_path = convert_to_text_file(contents)
        # Download button in Streamlit
        with st.sidebar:
            with open(transcript_file_path, "r") as file:
                st.download_button(
                    label="Download Transcript as Text",
                    data=file,
                    file_name="transcript.txt",
                    mime="text/plain",
                )
        # Creates a prompt from the video transcript and sends it to the LLM
        prompt = create_prompt(contents)
        output = chain(prompt)["response"]    
        st.session_state["previous"].append("Video received. Currently reviewing...")
        st.session_state["generated"].append(output)

    history = chain.memory.load_memory_variables({})["history"]

# Displays the conversation history in the Streamlit app by iterating over previous and generated messages.
if st.session_state["previous"]:
    with response_container:
        for i, (previous_message, generated_message) in enumerate(zip(st.session_state["previous"], st.session_state["generated"])):
            message(previous_message, is_user=True, key=f"{i}_user")
            message(generated_message, key=str(i))
        # Regular expression to capture content between 'Thumbnail Design' and 'Content Enhancement'
        pattern = r"Thumbnail Design:(.*?)Content Enhancement:"

        # Search for the pattern in the text
        match = re.search(pattern, output, re.DOTALL)

        if match:
            result = match.group(1).strip()
            generated_thumbnail = generate_thumbnail(f"Create a {result}")
            st.image(generated_thumbnail)
        else:
            print("No match found.")