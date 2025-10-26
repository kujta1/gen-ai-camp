
import streamlit as st
from main import LLMApp

if "messages" not in st.session_state:
    st.session_state.messages = []

if "llm_app" not in st.session_state:
    st.session_state.llm_app = None


st.set_page_config(
    page_title="GenAI Week 1 - Stupid LLM Chat Application",
    layout="centered"
)


with st.sidebar:
    st.title("GenAI Bootcamp")
    st.header("Week 1 Project")
    st.subheader("Stupid LLM Chat Application")
    st.markdown(
        """
        This is a simple chat application using a Large Language Model (LLM).
        You can enter your message and receive a response from the LLM.
        """
    )

    def on_model_change():
        st.session_state.messages = []

    model = st.selectbox(
        "Select Model",
        options=[
            "gpt5",
            "gpt5mini",
            "gpt5nano",
            "llama3.1",
            "llama3.3"
        ],
        index=4,
        on_change=on_model_change,
    )
    st.session_state.llm_app = LLMApp(model=model)
    if model not in ["gpt5", "gpt5mini", "gpt5nano"]:
        temperature = st.slider(
            " Select Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.05,
            help="Higher values makes the answer more diverse, and less similar with previous answers."
        )
    else:
        temperature = 1.0
    max_tokens = st.slider(
        "Select Max Tokens",
        min_value=512,
        max_value=2048,
        value=1024,
        step=128,
        help="Set the maximum number of tokens in the response."
    )
    system_prompt = st.text_area(
        "System Prompt",
        placeholder="You are a helpful assistant.",
        help="Set a role or context for the assistant."
    )
    if st.button("Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        # if st.session_state.llm_app:
        #     st.session_state.llm_app.clear_history()

        st.rerun()

if prompt := st.chat_input("Type your message here..."):
    st.session_state.messages.append(
        {
            "role": "user",
            "content": f"{prompt}"
        }
    )
    for message in st.session_state.messages[:-1]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    with st.chat_message("user"):
        st.markdown(prompt)

    # get assistant's response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.llm_app.chat(
                user_message=prompt,
                system_prompt=system_prompt if system_prompt else None,
                temperature=temperature,
                max_tokens=max_tokens
            )
            st.markdown(response)
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": f"{response}"
                }
            )
