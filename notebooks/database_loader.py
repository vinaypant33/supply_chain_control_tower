
'''
Optional Python Code to load the file to the mysql database  - The tables are predefined and just the data needs to be uploaded in mysql databse
- later on I used Mysql workben import wizaed to laod the file as it was easier and this file was deprecidated
'''

import pandas as pd
from sqlalchemy import create_engine

df = pd.read_csv("../data/supply_chain_dataset.csv")

engine = create_engine("mysql+mysqlconnector://root:datapassword@localhost/supplier_data")

df.to_sql("raw_data_supply_chain", con=engine, if_exists="append", index=False)

print("Data loaded successfully") 

