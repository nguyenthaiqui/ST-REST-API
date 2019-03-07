'''
@author: Kabaji
@email: nguyenthaiqui233@gmail.com
@version: 1.0
@since: Mar 5, 2019
'''
from flask import jsonify

import connector
from json import dumps
from JSONObject import json2obj

def addRecord(js_data):
    """input json include keys : username, style, distance, milisec, sec, min"""
    db, c = connector.connection()
    dict_cursor = connector.getDictCursor()
    dict_cursor.execute("SELECT id FROM distance WHERE swim_distance = %s", js_data['distance'])
    myDistanceID = dict_cursor.fetchone()
    dict_cursor.execute("SELECT id FROM style WHERE swim_name = %s", js_data['style'])
    myStyleID = dict_cursor.fetchone()
    dict_cursor.execute("SELECT id FROM `user` WHERE username = %s AND role_id = %s", (js_data['username'],2))
    myUserID = dict_cursor.fetchone()
    if myUserID:
        values = (js_data['milisec'], js_data['sec'], js_data['min'], myDistanceID['id'], myStyleID['id'], js_data['date'], myUserID['id'])
        c.execute("INSERT INTO `record`(swim_milisec,swim_sec,swim_min,style_id,distance_id,date_id,user_id) "
                  "VALUES(%s,%s,%s,%s,%s,%s,%s)",values)
        return jsonify({"result":"success"})
    else:
        return jsonify({"result":"unknown username"})
    return  jsonify({"result":"fail"})
