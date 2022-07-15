import pandas as pd
import sys
import os
from github import Github
import psycopg2 as pg
import pandas.io.sql as psql
sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config.credentials as credentials


def read_github_csv():
    url = "https://raw.githubusercontent.com/Osr-Tester/Data_Labelling/main/hansard_data.csv"
    df_github = pd.read_csv(url)
    return df_github

def read_heroku_db():
    conn = pg.connect(credentials.database_url)
    df_db = psql.read_sql("SELECT * FROM statistical_data", conn)
    return df_db

def get_updated_csv():
    df = read_github_csv()
    df_db = read_heroku_db()
    #
    df_new = pd.DataFrame({'clean_text': df.clean_text.drop_duplicates()}).reset_index().drop('index', axis=1)
    df_new = df_new[~df_new.clean_text.isin(df_db.clean_text.values)]
    df_to_update = df_new.to_csv('hanard_data.csv')
    # Automate the update to GitHub.
    org = "Osr-Tester"
    repo = "Data_labelling"
    branch = "main"
    file_path = "hansard_data.csv"

    token = credentials.access_token
    # Authenticates GitHub and updates file with df_string
    g = Github(token)
    repo = g.get_repo(f"{org}/{repo}")
    contents = repo.get_contents(file_path, ref=branch)
    #
    repo.update_file(path=file_path,
                     message="updating data",
                     content=df_to_update,
                     branch=branch,
                     sha=contents.sha)


if __name__ == '__main__':
    get_updated_csv()
