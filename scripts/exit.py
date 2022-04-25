import streamlit as st
import os
import pandas as pd
from github import Github
from github import InputGitTreeElement


def read_tweets():
    url = 'https://raw.githubusercontent.com/Hrdya-bhaskaran/data_labelling_app/main/tweets.csv'
    df = pd.read_csv(url, index_col=0)
    return df


def app():
    wrapper()


def wrapper():
    #st.write(st.session_state)
    df = read_tweets()
    for tweets, label in zip(st.session_state['tweets'][:-1], st.session_state['labels']):
        df.loc[df.clean_text == tweets, 'label'] = label
    tweets_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'tweets.csv')
    df_commit = df.to_csv(index=False)
    file_list = [df_commit]
    file_names = ["tweets.csv"]
    # Create connection with GiHub
    user = os.environ['git_user']
    password = os.environ['git_token']
    commit_message = 'Tweets file updated'
    g = Github(user, password)
    #
    repo = g.get_user().get_repo(os.environ['git_repo_name'])
    master_ref = repo.get_git_ref("heads/main")
    master_sha = master_ref.object.sha
    base_tree = repo.get_git_tree(master_sha)
    #
    element_list = list()
    element = InputGitTreeElement(file_names[0], '100644', 'blob', file_list[0])
    element_list.append(element)
    tree = repo.create_git_tree(element_list, base_tree)
    parent = repo.get_git_commit(master_sha)
    commit = repo.create_git_commit(commit_message, tree, [parent])
    master_ref.edit(commit.sha)
    print('Update complete')


    st.title('Thank you for helping us to label the data!')
    #st.write(st.session_state)
