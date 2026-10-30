import streamlit as st
from datahandler import DataHandler
from utils import build_prompt,get_ollama_response


st.set_page_config(page_title="Fitness Passport Agent")
st.title("Python Support Agent")

#cache the db so it loads once per session

@st.cache_resource

def load_db():
    return DataHandler()


handler = load_db()

if "messages" not in st.session_state:
    st.session_state.messages=[]


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt:=st.chat_input("What's up?"):
    st.session_state.messages.append({"role":"user","content" : prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching..."):
            docs,metas = handler.retrieve(prompt)
            final_prompt = build_prompt(prompt,docs)
            assistant_response = get_ollama_response(final_prompt)
            st.markdown(assistant_response)


    st.session_state.messages.append({"role":"assistant","content" : assistant_response})
