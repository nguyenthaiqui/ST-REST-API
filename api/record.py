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


def add(username, data):
    '''input json key : lesson_id,repetition, username, exercise_id, swim_millisec, swim_sec, swim_min, heart_beat_id '''

    db, c = connector.connection()
    dict_cursor = connector.getDictCursor()

    dict_cursor.execute("SELECT * FROM `user` WHERE username = %s", username)
    coach = dict_cursor.fetchone()

    for i in data:
        dict_cursor.execute("SELECT * FROM `user` WHERE username = %s AND role_id = %s", (i['username'], 2))
        user = dict_cursor.fetchone()

        dict_cursor.execute("SELECT * FROM `lesson_plan` WHERE id = %s AND coach_id = %s", (i['lesson_id'],coach['id']))
        myLesson = dict_cursor.fetchone()

        if not myLesson:
            db.close()
            return jsonify(
                {
                    "values": "",
                    "success": False,
                    "errorMessage": "Invalid lesson_name",
                    "message": None
                }
            )
        dict_cursor.execute("SELECT COUNT(*) FROM `record` WHERE user_id = %s AND lesson_id =%s AND exercise_id= %s",
                            (user['id'], myLesson['id'], i['exercise_id']))
        myRep = dict_cursor.fetchone()['COUNT(*)']
        dict_cursor.execute("SELECT * FROM `exercise` WHERE lesson_id = %s",myLesson['id'])
        myExercise = dict_cursor.fetchone()
        if myRep < myExercise['repetition']:
            c.execute(
                "INSERT INTO `record` (swim_millisec,swim_sec,swim_min,heart_beat_id,exercise_id,lesson_id,user_id,coach_id) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s,%s)",
                (i['swim_millisec'], i['swim_sec'], i['swim_min'], i['heart_beat_id'], i['exercise_id'],myLesson['id'],user['id'],coach['id']))
            db.commit()
        else:
            db.close()
            return jsonify(
                {
                    "values": "",
                    "success": False,
                    "errorMessage": "Max record of lesson : "+myLesson['name'],
                    "message": None
                }
            )
    db.close()
    return jsonify(
        {
            "values": "added records in lesson: " + myLesson['name'],
            "success": True,
            "errorMessage": "",
            "message": None
        }
    )
