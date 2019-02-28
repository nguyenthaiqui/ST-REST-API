'''
@author: Evan, Kabaji
@version: 1.0
@since: Jan 19, 2019
'''
import pymysql


def connection():
    db = pymysql.connect(host="localhost",
                         user="root",
                         passwd="123456",
                         database="swimtracker",
                         charset='utf8mb4',)
    c = db.cursor()
    return db, c

def getDictCursor():
    """The cursor which fetch data to dict"""
    db, c = connection()
    dict_cursor = db.cursor(pymysql.cursors.DictCursor)
    return dict_cursor