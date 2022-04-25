import streamlit as st
import pandas as pd
import os
import numpy as np
import re





def app():
    wrapper()



def clean_tweets(df):
    if 'text' in df.columns:
        df['clean_text'] = df['text'].apply(lambda x: re.split('https:\/\/.*', str(x))[0])
        df.drop_duplicates('clean_text', inplace=True)
    if 'text' and 'entities_hashtags' in df.columns:
        df.drop(['text', 'entities_hashtags'], axis=1, inplace=True)
    df.reset_index(inplace=True)
    df['label'] = np.nan
    tweets_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'tweets.csv')
    df.to_csv(tweets_file, index=False)
    return df


def read_tweets():
    url = 'https://raw.githubusercontent.com/Hrdya-bhaskaran/data_labelling_app/main/tweets.csv'
    df = pd.read_csv(url, index_col=0)
    return df


def write_tweets(df):
    tweets_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'tweets.csv')
    df.to_csv(tweets_file, index=False)


def wrapper():
    if 'labels' not in st.session_state:
        st.session_state['labels'] = []
    if 'tweets' not in st.session_state:
        st.session_state['tweets'] = []
    if 'count' not in st.session_state:
        st.session_state['count'] = [-1]
    df = read_tweets()
    ct = 0
    count = np.random.randint(df.shape[0])
    if 'label' not in df.columns:
        df = clean_tweets(df)
    st.session_state['submit'] = False
    st.title('Welcome to the Fun of labelling!!')
    st.write('Tweet text:')
    while count in st.session_state['count']:
        if ct > df.shape[0]: break
        count = np.random.randint(df.shape[0])
        ct += 1
    st.write(df['clean_text'][count])
    st.session_state['tweets'].append(df['clean_text'][count])
    st.session_state['count'].append(count)

    with st.form(key='my_form', clear_on_submit=True):
        select_quality = st.radio(
            "Is this tweet about quality of statistics?", ('Yes', 'No', 'I don\'t know'))
        submit_button = st.form_submit_button(label='Submit')

        if submit_button:
            st.session_state['submit'] = True
            st.session_state['labels'].append(select_quality)
            #st.session_state['tweets'].append(df['clean_text'][count])
            #st.write(st.session_state)
    # stop = st.button('Exit')
    # if stop:
    #     df = read_tweets()
    #     for tweets, label in zip(st.session_state['tweets'], st.session_state['labels']):
    #         df.loc[df.clean_text == tweets, 'label'] = label
    #     tweets_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'tweets_for_ml.csv')
    #     df.to_csv(tweets_file, index=False)
       # exit.app()
