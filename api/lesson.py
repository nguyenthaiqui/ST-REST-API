'''
@author: Kabaji
@email: nguyenthaiqui233@gmail.com
@version: 1.0
@since: Mar 19, 2019
'''
import connector
from flask import jsonify
import datetime

def add(data, username, team_id):
    db,c = connector.connection()
    dict_cursor = connector.getDictCursor()

    dict_cursor.execute("SELECT * FROM `user` WHERE username = %s",username)
    coach = dict_cursor.fetchone()

    c.execute("SELECT * FROM `lesson_plan` WHERE name = %s AND coach_id = %s AND team_id = %s",(data['name'],coach['id'],team_id))
    myLesson = c.fetchall()
    if not myLesson:
        c.execute("INSERT INTO `lesson_plan` (name,date,created_at,coach_id,team_id) VALUES (%s,%s,%s,%s,%s)",
                  (data['name'],data['date'],str(datetime.datetime.now()),coach['id'],team_id))
        db.commit()
        db.close()
        return jsonify(
            {
                "values": "Lesson " + data['name'] + " has created",
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

def edit(data,username, team_id,lesson_id):
    db,c = connector.connection()
    dict_cursor = connector.getDictCursor()

    dict_cursor.execute("SELECT * FROM `lesson_plan` WHERE id = %s",lesson_id)
    myLesson = dict_cursor.fetchone()

    if myLesson:
        c.execute("UPDATE `lesson_plan` SET name = %s, date = %s, updated_at = %s",(data['name'],data['date'],str(datetime.datetime.now())))
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

    dict_cursor.execute("SELECT * FROM `lesson_plan` WHERE id = %s", lesson_id)
    myLesson = dict_cursor.fetchone()

    if myLesson:
        c.execute("DELETE FROM `lesson_plan` WHERE id = %s",lesson_id)
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



