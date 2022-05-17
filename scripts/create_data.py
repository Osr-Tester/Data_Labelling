import os
import sys
import psycopg2
sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config.credentials as credentials

conn = psycopg2.connect(credentials.database_url)
cur = conn.cursor()
create_table_statement = "CREATE TABLE statistical_data (clean_text text PRIMARY KEY, label text)"
cur.execute(create_table_statement)
conn.commit()
conn.close()
