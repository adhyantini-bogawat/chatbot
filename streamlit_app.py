import streamlit as st
import replicate
import os

# App title
st.set_page_config(page_title=" Llama 3 Chatbot")

# Replicate Credentials
with st.sidebar:
    st.title('Llama 3 Chatbot')
    st.write('This chatbot is intended to assist you with anny queries')
    if 'REPLICATE_API_TOKEN' in st.secrets:
        st.success('API key already provided!', icon='✅')
        replicate_api = st.secrets['REPLICATE_API_TOKEN']
    else:
        replicate_api = st.text_input('Enter Replicate API token:', type='password')
        if not (replicate_api.startswith('r8_') and len(replicate_api)==40):
            st.warning('Please enter your credentials!', icon='⚠️')
        else:
            st.success('Proceed to entering your prompt message!', icon='👉')
    os.environ['REPLICATE_API_TOKEN'] = replicate_api

    st.subheader('Models and parameters')
    selected_model = st.sidebar.selectbox('Choose a Llama 3 model', ['meta-llama-3-8b-instruct', 'meta-llama-3-8b'], key='selected_model')
    if selected_model == 'meta-llama-3-8b-instruct':
        llm = 'meta/meta-llama-3-8b-instruct'
    elif selected_model == 'meta-llama-3-8b':
        llm = 'meta/meta-llama-3-8b'
    # temperature = st.sidebar.slider('temperature', min_value=0.01, max_value=1.0, value=0.1, step=0.01)
    # top_p = st.sidebar.slider('top_p', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
    # max_length = st.sidebar.slider('max_length', min_value=32, max_value=128, value=120, step=8)
    temperature = 0.1
    top_p = 0.9
    max_length = 120

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "tutor", "content": "What would you like to learn about today?"}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "tutor", "content": "What would you like to learn about today?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# Function for generating LLaMA2 response. Refactored from https://github.com/a16z-infra/llama2-chatbot
def generate_llama2_response(prompt_input):
    string_dialogue = "You are a smart teacher who knows a lot of general knowledge. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'tutor'."
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "Tutor: " + dict_message["content"] + "\n\n"
    output = replicate.run(f'meta/{selected_model}', 
                           input={"prompt": f"{string_dialogue} {prompt_input} Tutor: ",
                                  "temperature":temperature, "top_p":top_p, "max_length":max_length, "repetition_penalty":1})
    return output

# User-provided prompt
if prompt := st.chat_input(disabled=not replicate_api):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "tutor":
    with st.chat_message("tutor"):
        with st.spinner("Thinking..."):
            response = generate_llama2_response(prompt)
            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    message = {"role": "tutor", "content": full_response}
    st.session_state.messages.append(message)
