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
    db,c = connector.connection()
    dict_cursor = connector.getDictCursor()

    dict_cursor.execute("SELECT * FROM `user` WHERE username = %s",username)
    coach = dict_cursor.fetchone()
    c.execute("SELECT * FROM `lesson` WHERE name = %s AND coach_id = %s ",(data['lesson_name'],coach['id']))
    myLesson = c.fetchall()
    if not myLesson:
        c.execute("INSERT INTO `lesson` (name,created_at,coach_id) VALUES (%s,%s,%s)",
                  (data['lesson_name'],str(datetime.datetime.now()),coach['id'],))
        db.commit()
        db.close()
        return jsonify(
            {
                "values": "Lesson " + data['lesson_name'] + " has created",
                "success": True,
                "errorMessage": "",
                "message": None
            }
        )
    db.close()
    return jsonify(
        {
            "values": "",
            "success": False,
            "errorMessage": "The lesson exist",
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



