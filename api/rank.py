'''
@author: Kabaji
@email: nguyenthaiqui233@gmail.com
@version: 1.0
@since: Apr 4, 2019
'''
from flask import jsonify

import connector


def getRank():
    dict_cursor = connector.getDictCursor()

    dict_cursor.execute("SELECT * FROM `rank`")
    myRank = dict_cursor.fetchall()
    dict_cursor.close()
    return jsonify(myRank)