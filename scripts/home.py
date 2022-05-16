import streamlit as st
import pandas as pd
import os
import numpy as np
import re
import time


def app(df):
    wrapper(df)


def wrapper(df):
    if 'labels' not in st.session_state:
        st.session_state['labels'] = []
    if 'tweets' not in st.session_state:
        st.session_state['tweets'] = []
    if 'count' not in st.session_state:
        st.session_state['count'] = [-1]
    ct = 0
    count = np.random.randint(df.shape[0])
    #
    st.title('Welcome to the Fun of labelling!!')
    st.write('Text:')
    while count in st.session_state['count']:
        if ct > df.shape[0]: break
        count = np.random.randint(df.shape[0])
        ct += 1
    #st.write(df.columns)
    st.write(df.clean_text[count])
    st.session_state['tweets'].append(df['clean_text'][count])
    st.session_state['count'].append(count)

    with st.form(key='my_form', clear_on_submit=True):
        select_quality = st.radio(
            "Is there statistical content in this text?", ('Yes', 'No', 'I don\'t know'))
        submit_button = st.form_submit_button(label='Submit')

        if submit_button:
            st.session_state['labels'].append(select_quality)
            time.sleep(2)

    st.markdown("_Please select the drop down - **Exit** when done with labelling, thank you!_")
