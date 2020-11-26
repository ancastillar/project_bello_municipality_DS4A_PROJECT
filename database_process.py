import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn.metrics as Metrics
import pandas as pd
import matplotlib.pyplot as plt
import unidecode
from sqlalchemy import create_engine, text
import streamlit as st

class DATABASE:

    def __init__(self, endpoint, user, password, db, port=5432):
        self.engine = create_engine(f'postgresql://{user}:{password}@{endpoint}:{port}/{db}')

    #===================================#
    #     Postgres data reader          #
    #===================================#
    def db_read(self, query):
        return pd.read_sql(query, self.engine)

    #===================================#
    #     Postgres query executor       #
    #===================================#
    def db_execute(self, query):
        mydb = self.engine.raw_connection()
        mycursor = mydb.cursor()
        mycursor.execute(query)
        mydb.commit()
        mycursor.close()
        mydb.close()
        
    #===================================#
    #     Postgres data writer          #
    #===================================#
    def db_upload(self, df, table, ignore_duplicates=True):
        #### Column match           ing
        col_order = self.db_read(f'SELECT * FROM {table} LIMIT 1;').columns.tolist()
        df = df[col_order]

        #### Start connection
        mydb = self.engine.raw_connection()
        mycursor = mydb.cursor()

        #df.head(0).to_sql(table, con=self.engine, if_exists='append', index=False)

        output = io.StringIO()
        df.to_csv(output, sep='|', header=False, index=False, na_rep='null')
        output.seek(0)

        try:
            mycursor.copy_from(output, table, sep='|', null='null')
            mydb.commit()
            error = ''
            status = True
        except Exception as e:
            mycursor.close()
            mydb.close()
            error = str(e)
            status = False

        #### Insert even if there are duplicates
        if ('duplicate key value violates unique constraint' in error) and ignore_duplicates:
            mydb = self.engine.raw_connection()
            mycursor = mydb.cursor()
            contents = output.getvalue().split('\n')[:-1]
            for row in contents:
                row = "'" + row.replace("|", "','") + "'"
                row = row.replace("'null'", "NULL")
                query = f'INSERT INTO {table} VALUES ({row}) ON CONFLICT DO NOTHING;'
                mycursor.execute(query)
                mydb.commit()
            status = True

        mydb.close()
        return status
