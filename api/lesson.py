'''
@author: Kabaji
@email: nguyenthaiqui233@gmail.com
@version: 1.0
@since: Mar 19, 2019
'''
import connector
from flask import jsonify
import datetime

def view(username):
    db,c =connector.connection()
    dict_cursor = connector.getDictCursor()

    dict_cursor.execute("SELECT id FROM `user` WHERE username = %s", username)
    coach = dict_cursor.fetchone()

    dict_cursor.execute("SELECT * FROM `lesson` WHERE coach_id = %s", coach['id'])
    myListLesson = dict_cursor.fetchall()

    for i in myListLesson:
        dict_cursor.execute("SELECT name FROM `team` WHERE coach_id = %s", i['coach_id'])

    db.close()
    return jsonify(myListLesson)



def add(data, username):
    db, c = connector.connection()
    dict_cursor = connector.getDictCursor()

    dict_cursor.execute("SELECT * FROM `user` WHERE username = %s", username)
    coach = dict_cursor.fetchone()
    c.execute("SELECT * FROM `lesson` WHERE name = %s AND coach_id = %s ", (data['lesson_name'], coach['id']))
    myLesson = c.fetchall()
    if not myLesson:
        c.execute("INSERT INTO `lesson` (name,created_at,coach_id) VALUES (%s,%s,%s)",
                  (data['lesson_name'], str(datetime.datetime.now()), coach['id'],))
        db.commit()
    dict_cursor.close()
    db.close()
    db2, c = connector.connection()
    dict_cursor2 = connector.getDictCursor()
    dict_cursor2.execute("SELECT * FROM `lesson` WHERE name = %s", data['lesson_name'])
    myLesson2 = dict_cursor2.fetchone()
    for i in data['exercise']:
        c.execute("SELECT * FROM `exercise` WHERE type_id = %s AND lesson_id = %s", (i['type_id'], myLesson2['id']))
        if not c.fetchall():
            dict_cursor2.execute("SELECT id FROM `distance` WHERE swim_distance = %s", i['distance'])
            myDistanceID = dict_cursor2.fetchone()
            dict_cursor2.execute("SELECT id FROM `style` WHERE swim_name = %s", i['style'])
            myStyleID = dict_cursor2.fetchone()
            c.execute(
                "INSERT INTO `exercise` (style_id,distance_id,repetition,description,type_id,lesson_id) VALUES(%s,%s,%s,%s,%s,%s)",
                (myStyleID['id'], myDistanceID['id'], i['repetition'], i['description'], i['type_id'], myLesson2['id']))
            db2.commit()
        else:
            dict_cursor2.close()
            db2.close()
            return jsonify(
                {
                    "values": "",
                    "success": False,
                    "errorMessage": "",
                    "message": None
                }
            )
    db2.close()
    return jsonify(
        {
            "values": myLesson2,
            "success": True,
            "errorMessage": "",
            "message": None
        }
    )


def edit(data,username,lesson_id):
    db,c = connector.connection()
    dict_cursor = connector.getDictCursor()

    dict_cursor.execute("SELECT * FROM `lesson` WHERE id = %s",lesson_id)
    myLesson = dict_cursor.fetchone()

    if myLesson:
        c.execute("UPDATE `lesson` SET name = %s, updated_at = %s WHERE id = %s",(data['name'],str(datetime.datetime.now()),lesson_id))
        db.commit()
        db.close()
        return jsonify(
            {
                "values": "Lesson " + myLesson['name'] + " has changed",
                "success": True,
                "errorMessage": "",
                "message": None
            }
        )
    return jsonify(
        {
            "values": "",
            "success": False,
            "errorMessage": "Invalid lesson",
            "message": None
        }
    )

def delete(lesson_id):
    db,c =connector.connection()
    dict_cursor = connector.getDictCursor()

    dict_cursor.execute("SELECT * FROM `lesson` WHERE id = %s", lesson_id)
    myLesson = dict_cursor.fetchone()

    if myLesson:
        c.execute("DELETE FROM `lesson` WHERE id = %s",lesson_id)
        c.execute("DELETE FROM `exercise` WHERE lesson_id = %s",lesson_id)
        db.commit()
        db.close()
        return jsonify(
            {
                "values": "Lesson " + myLesson['name'] + " has deleted",
                "success": True,
                "errorMessage": "",
                "message": None
            }
        )
    return jsonify(
        {
            "values": "",
            "success": False,
            "errorMessage": "Invalid lesson",
            "message": None
        }
    )



