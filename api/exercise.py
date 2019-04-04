'''
@author: Kabaji
@email: nguyenthaiqui233@gmail.com
@version: 1.0
@since: Mar 20, 2019
'''

import connector
from flask import jsonify

def getType():
    db, c = connector.connection()
    """get all databases from table exercise_type and convert to json"""
    c.execute("SELECT * FROM exercise_type")
    myTyle = c.fetchall()
    columns = ['id', 'type_name']
    # columns = [column[0] for column in c.description]        #get keys in db
    info = [dict(zip(columns, row)) for row in myTyle]  # create zip with key & value => convert dict
    db.close()
    c.close()
    return jsonify(info)