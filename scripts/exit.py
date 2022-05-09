import streamlit as st
import os
import pandas as pd
from datetime import datetime
from github import Github
from github import InputGitTreeElement
import time
import psycopg2

database_url = os.environ.get('DATABASE_URL')


def app(df):
    wrapper(df)


def wrapper(df):
    conn = psycopg2.connect(database_url)
    cur = conn.cursor()
    for tweets, label in zip(st.session_state['tweets'][:-1], st.session_state['labels']):
        try:
            cur.execute("INSERT INTO statistical_data(clean_text, label) VALUES (%s, %s)", (tweets, label))
        except:
            continue
    conn.commit()
