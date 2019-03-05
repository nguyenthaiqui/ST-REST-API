'''
@author: Kabaji
@email: nguyenthaiqui233@gmail.com
@version: 1.0
@since: Mar 5, 2019
'''

import connector
from json import dumps
from JSONObject import json2obj


def addRecord(data):
    db, c = connector.connection()
    object_data = json2obj(dumps(data))
    c.execute("SELECT id FROM distance WHERE swim_distance = %s",data['distance'])
    myDistanceID = c.fetchall()
    c.execute("SELECT id FROM style WHERE swim_name = %s",data['style'])
    myStyleID = c.fetchall()
    values = (data['milisec'],data['sec'],data['min'],myStyleID[0][0],myDistanceID[0][0],data['date'],data['user_id'])
    c.execute("INSERT INTO `record`(swim_milisec,swim_sec,swim_min,style_id,distance_id,date_id,user_id) "
              "VALUES(%s,%s,%s,%s,%s,%s,%s)",values)

    return ''
