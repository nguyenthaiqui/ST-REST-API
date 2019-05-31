'''
@author: Kabaji
@email: nguyenthaiqui233@gmail.com
@version: 1.0
@since: Feb 20, 2019
'''
import connector
from flask import jsonify


def getDistance():
   db, c = connector.connection()
   """get all databases from table age and convert to json"""
   c.execute("SELECT * FROM distance")
   myDistance = c.fetchall()
   columns = ['id','swim_distance']
   #columns = [column[0] for column in c.description]        #get keys in db
   info =[dict(zip(columns, row)) for row in myDistance]        #create zip with key & value => convert dict
   db.close()
   c.close()
   return jsonify(info)