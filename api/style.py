'''
@author: Kabaji
@email: nguyenthaiqui233@gmail.com
@version: 1.0
@since: Mar 5, 2019
'''
import connector
from flask import jsonify


def getStyle():
   db, c = connector.connection()
   """get all databases from table age and convert to json"""
   c.execute("SELECT * FROM style")
   myStyle = c.fetchall()
   columns = ['id','swim_name']
   #columns = [column[0] for column in c.description]        #get keys in db
   info =[dict(zip(columns, row)) for row in myStyle]        #create zip with key & value => convert dict
   return jsonify(info)