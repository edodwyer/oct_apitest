from sqlalchemy import create_engine
import pymysql
import pandas as pd
import credentials


def get_sql_dat(dStart,dEnd):
    user = credentials.user
    password = credentials.password
    address= credentials.address
    dbschem = credentials.dbschem
    
#     'mysql://%s:%s@%s' % (USER, PASSWORD, HOST)
    sqlEngine = create_engine('mysql+pymysql://'+user+':'+password+'@'+address+dbschem, pool_recycle=3306)
    
    synth_demand=pd.read_sql("SELECT * FROM SyntheticDemand where DateTime between "+f"'{dStart}'"+" and "+f"'{dEnd}'", con=sqlEngine,index_col='DateTime')
    
    return synth_demand

