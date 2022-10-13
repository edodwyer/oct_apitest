from sqlalchemy import create_engine
import pymysql
import pandas as pd
import datetime as dt
import pickle
import credentials


user = credentials.user
password = credentials.password
address= credentials.address
dbschem = credentials.dbschem

#%%
synth_dem = pickle.load(open("synth_dem.p","rb"))

tableName = "SyntheticDemand"

df = synth_dem
 
sqlEngine = create_engine('mysql+pymysql://'+user+':'+password+'@'+address+dbschem, pool_recycle=3306)

dbConnection = sqlEngine.connect()


try:
    frame = df.to_sql(tableName, dbConnection, if_exists='fail');

except ValueError as vx:
    print(vx)

except Exception as ex:
    print(ex)

else:
    print("Table %s created successfully."%tableName);   

finally:
    dbConnection.close()
  