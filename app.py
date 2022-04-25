import streamlit as st
from multiapp import MultiApp
from scripts import home, exit  # import your app modules here

app = MultiApp()

if 'labels' not in st.session_state:
    st.session_state['labels'] = []
if 'tweets' not in st.session_state:
    st.session_state['tweets'] = []
if 'count' not in st.session_state:
    st.session_state['count'] = [-1]
# Add all your application here
app.add_app("Home", home.app)
app.add_app("Exit", exit.app)
# The main app
app.run()
