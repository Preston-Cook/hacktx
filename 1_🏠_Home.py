import streamlit as st


st.set_page_config(page_title='Parlom: Home', page_icon=':house:',
                   layout="wide", initial_sidebar_state="auto", menu_items=None)

with st.container():
    st.title('Parlom')

with st.container():
    st.markdown(
            """
            Parlom is an in-browser tool that allows users to speak with OpenAI's GPT-3 Model

            ### How does it work?
            Parlom uses AssemblyAI's real-time speech recognition API in conjunction with Google's text-to-speech API to send and read data from GPT-3. 
            ### Want to see more awesome projects?
            Feel free to check out my [GitHub](https://github.com/Preston-Cook) or [LinkedIn](https://www.linkedin.com/in/preston-l-cook/)
        """
        )