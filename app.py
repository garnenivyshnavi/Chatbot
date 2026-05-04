import streamlit as st
from google import genai

# --- 1. Configuration ---
# Use the newer Client class
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
for model in client.models.list():
    print(model.name)



st.set_page_config(page_title="Gemini 2.5/3 Chat", page_icon="♊")
st.title("Google Gemini Assistant")

# --- 2. Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. Display History ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. Chat Logic ---
if prompt := st.chat_input("Ask Gemini anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        # Using Gemini 2.5 Flash (highly capable and free)
        # You can also try 'gemini-3-flash-preview' for the latest model
        response = client.models.generate_content_stream(
            model='gemini-2.5-flash',
            contents=prompt,
            config={'system_instruction': 'You are a helpful assistant.'}
        )
        
        for chunk in response:
            full_response += chunk.text
            placeholder.markdown(full_response + "▌")
        
        placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
