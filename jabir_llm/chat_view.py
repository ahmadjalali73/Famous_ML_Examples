import streamlit as st
import requests
import json

base_url = 'https://api.jabirproject.org/generate'
api_code = 'XXX-XXX-XXX'
headers = {
    'Content-Type': 'application/json',
    'apikey': api_code
}

st.title("Jabir Bot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Say something"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    data = {
        'messages': [
            {'role': 'user', 'content': prompt}
            ]
    }

    answer = ""
    response = requests.post(base_url, headers=headers, data=json.dumps(data))
    if response.ok:
        answer = {'content': response.json()['result']['content'], 'role': response.json()['result']['role']}
    else:
        answer = {'content': 'NO ANSWER FROM BOT', 'role': 'assistant'}
    
    display_answer = answer['content']
    with st.chat_message("assistant"):
        st.markdown(display_answer)

    st.session_state.messages.append({"role": answer['role'], "content": answer['content']})