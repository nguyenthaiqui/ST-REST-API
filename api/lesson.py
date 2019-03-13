'''
@author: Evan
@email: lenguyenhoangvan18@gmail.com
@version: 1.0
@since: Feb 21, 2019
'''
import connector
from flask import jsonify
from JSONObject import json2obj  # json2obj recive a string
from json import dumps
import datetime


def create_lesson(data,username):
    db, c = connector.connection()
    dict_cursor = connector.getDictCursor()
    obj_data = json2obj(dumps(data))
    dict_cursor.execute("SELECT id FROM `user` WHERE username = %s",username)
    coach = dict_cursor.fetchone()
    try:
        c.execute('''INSERT INTO lesson_plan (name, `date`, style_id, distance_id,
                                             repetition, age, description, create_at,coach_id)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                     (obj_data.lesson.name, str(datetime.datetime.now()), obj_data.lesson.style_id,
                     obj_data.lesson.distance_id, 1, obj_data.lesson.team_name,
                     obj_data.lesson.description, str(datetime.datetime.now())),coach['id'])
        db.commit()
    except:
        db.rollback()
        return jsonify({'result': {'status': 'fail'}})
    return jsonify({'result': {'status': 'success'}})


def increase_repetition(team,username):
    db, c = connector.connection()
    dict_cursor = connector.getDictCursor()
    dict_cursor.execute("SELECT id FROM `user` WHERE username = %s", username)
    coach = dict_cursor.fetchone()
    c.execute('''SELECT repetition 
                 FROM lesson_plan 
                 WHERE team = %s AND coach_id = %s''')
    my_repe = c.fetchall()
    try:
        c.execute('''UPDATE lesson_plan
                     SET repetition, update_at
                     WHERE team = %s''', (my_repe[0][0] + 1, str(datetime.datetime.now()), team))
        db.commit()
    except:
        db.rollback()



