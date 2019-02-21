'''
@author: Evan
@email: lenguyenhoangvan18@gmail.com
@version: 1.0
@since: Feb 20, 2019
'''
import connector
from flask import jsonify
from JSONObject import json2obj  # json2obj recive a string
from json import dumps


def add(data):
	db, c = connector.connection()
    obj_data = json2obj(dumps(data))
    


def delete(data):
	db, c = connector.connection()
    obj_data = json2obj(dumps(data))