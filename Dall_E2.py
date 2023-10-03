
import openai
# Set your OpenAI API key
openai.api_key = st.secrets("OPEN_AI_KEY")

import streamlit as st


biodatas=""
url=""


st.header("Generate AI Image")
st.markdown("---")

description = st.text_input(
    label='Enter description here...',
    max_chars=300,
    key='coach-description',
    help='This is a help tooltip for the input field.'
)

button_clicked = st.button("Generate!", on_click=lambda: generateAvatar(description))


def generateAvatar(description):
    prompt = "A photorealistic image of an single person - who is an executive coach with the following description"+description

    response = openai.Image.create(prompt=prompt)

    url = response["data"][0]["url"]
    width = 400
    height = 500
    st.markdown(f'<img src="{url}" width="{width}" height="{height}">', unsafe_allow_html=True)



    # st.image(url, width=400, height=500)

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Create a fictional Name and short resume of an executive coach under 50 words that matches the following description: {description}"}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Make sure to use a chat-based engine
        messages=messages
    )    
    

    biodatas = response['choices'][0]['message']['content']
    st.write(biodatas)
