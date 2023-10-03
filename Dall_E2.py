
import openai
# Set your OpenAI API key
import streamlit as st
import os


openai.api_key = st.secrets["OPEN_AI_KEY"]

biodata=""
url=""
global_message ="Please enter the password to continue..!"

def check_password():
    def password_entered():
        """Checks whether a password entered by the user is correct."""
    if st.session_state["password"] == st.secrets.get("password", "default_value"):
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        global global_message
        global_message = "😕 Password incorrect"
        return False
    else:
        # Password correct.
        return True

password_valid = check_password()


if not password_valid:
        st.error(global_message)

def generateAvatar(description):
    prompt = "A photorealistic image of an single person - who is an executive coach with the following description"+description

    response = openai.Image.create(prompt=prompt)

    url = response["data"][0]["url"]
    width = 400
    height = 500
    st.markdown(f'<img src="{url}" width="{width}" height="{height}" style="border-radius: 50%; width: 300px; height: 300px;">', unsafe_allow_html=True)



    # st.image(url, width=400, height=500)

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Create a fictional Name and short resume of an executive coach under 50 words that matches the following description: {description}"}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Make sure to use a chat-based engine
        messages=messages
    )    
    

    biodata = response['choices'][0]['message']['content']
    st.write(biodata)

st.header("Generate AI Image")
st.markdown("---")

description = st.text_input(
    label='Enter description here...',
    max_chars=300,
    key='coach-description',
    help='This is a help tooltip for the input field.',
    disabled=not password_valid
)

if st.button("Generate!", disabled=not password_valid):
    generateAvatar(description)
