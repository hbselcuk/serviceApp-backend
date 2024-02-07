
from sqlalchemy import create_engine
import psycopg2 
from psycopg2.extras import RealDictCursor

import json

db_conn = {'dbname':'serviceApp', 'user':'root', 'host':'62.171.190.234', 'port':'54321', 'password':'service3000'}

def executeQuery(query):
    cur = None
    try:
        connect = psycopg2.connect(**db_conn)
        cur = connect.cursor(cursor_factory = RealDictCursor)
        cur.execute(query)
        pg_data = cur.fetchall()
        connect.commit()
        print("PG data loaded:", query)
        print(pg_data)
        return pg_data
    except psycopg2.Error as e:
        print("Error:", e)
        return None  # Return something or raise an exception if needed
    finally:
        if cur:
            cur.close()
        if connect:
            connect.close()
        print("proceed!")
        

def getPGData(pg_Query,action,id):
    getstuff = "SELECT * FROM rest_api.getStuff(%s,%s)" % (action,id)  
    print (getstuff,type(getstuff))
    if pg_Query == 100:
        print(getstuff)
        result = executeQuery(getstuff)
        return result
    else:
        print("query not valid")
        return ("query not valid!")
        
def doStuffWithData(pg_Query, action, brian, some_ID):
    
    savestuff = "SELECT * FROM rest_api.saveStuff(%s,%s)" % (action, brian)
    updatestuff = "SELECT * FROM rest_api.updateStuff(%s,%s,%s)" % (action, some_ID, brian)

    if pg_Query == 200:
        print(savestuff)
        result = executeQuery(savestuff)
        return result
    elif pg_Query == 300:
        print(updatestuff)
        result = executeQuery(updatestuff)
        return result
    else:
        print("query not valid")
        return ("query not valid!")
    