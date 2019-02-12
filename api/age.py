import connector
from flask import jsonify



 def get():
    db, c = connector.connection()
    """get all databases from table age and convert to json"""
    c.execute("SELECT * FROM age")
    mydata = c.fetchall()
    columns = ['id','range_age']
    #columns = [column[0] for column in c.description]        #get keys in db
    info =[dict(zip(columns, row)) for row in mydata]        #create zip with key & value => convert dict
    return jsonify(info)                                     #return json with keys(id,age_range)