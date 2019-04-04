'''
@author: Kabaji
@email: nguyenthaiqui233@gmail.com
@version: 1.0
@since: Apr 4, 2019
'''
from flask import jsonify

import connector


def getHeartBeat():
    dict_cursor = connector.getDictCursor()

    dict_cursor.execute("SELECT * FROM `heart_beat`")
    myHeartBeat = dict_cursor.fetchall()
    dict_cursor.close()
    return jsonify(myHeartBeat)