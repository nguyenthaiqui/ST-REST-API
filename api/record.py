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



def add(username,data):
    '''input json key : lesson_id,repetition, username, exercise_id, milisec, sec, min, heart_beat_id '''
    db, c = connector.connection()
    dict_cursor = connector.getDictCursor()

    dict_cursor.execute("SELECT * FROM `user` WHERE username = %s", username)
    myCoach = dict_cursor.fetchone()
    for record in data['record']:
        dict_cursor.execute("SELECT * FROM `user` WHERE `id`= %s AND role_id = 2",record['user_id'])
        mySwimmer = dict_cursor.fetchone()
        dict_cursor.execute("SELECT COUNT(*) FROM `record` WHERE user_id = %s AND exercise_id =%s ",
                            (mySwimmer['id'], data['exercise_id']))
        myRep = dict_cursor.fetchone()['COUNT(*)']
        dict_cursor.execute("SELECT * FROM `exercise` WHERE id= %s ", data['exercise_id'])
        myExercise = dict_cursor.fetchone()
        if myRep < myExercise['repetition']:
            c.execute(
                "INSERT INTO `record` (user_id, coach_id, lesson_id, exercise_id, swim_millisec , swim_sec , swim_min, heart_beat_id ) VALUES (%s, %s, %s, %s, %s, %s, %s ,%s)",
                (record['user_id'],myCoach['id'],data['lesson_id'],data['exercise_id'], record['millisec'], record['sec'], record['min'], record['heart_beat_id']))
            db.commit()
        else:
            dict_cursor.close()
            c.close()
            db.close()
            return jsonify(
                {
                    "values": "",
                    "success": False,
                    "errorMessage": "",
                    "message": None
                }
            )
    dict_cursor.close()
    c.close()
    db.close()
    return jsonify(
        {
            "values": "",
            "success": True,
            "errorMessage": "",
            "message": None
        }
    )

