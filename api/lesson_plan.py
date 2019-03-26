'''
@author: Kabaji
@email: nguyenthaiqui233@gmail.com
@version: 1.0
@since: Mar 19, 2019
'''
import connector
from flask import jsonify
import datetime

def add(username,lesson_id,team_id,data):
    db,c = connector.connection()
    dict_cursor = connector.getDictCursor()

    dict_cursor.execute("SELECT * FROM `lesson-team` WHERE team_id = %s AND lesson_id = %s ",(team_id,lesson_id))
    if not dict_cursor.fetchone():
        c.execute("INSERT INTO `lesson-team` (lesson_id,team_id,date) VALUES (%s, %s, %s)",(lesson_id,team_id,data['date']))
        db.commit()
        db.close()
        return jsonify(
            {
                "values": "",
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
            "errorMessage": "this team already has the same lesson",
            "message": None
        }
    )

def view(team_id):
    db, c = connector.connection()
    dict_cursor = connector.getDictCursor()

    dict_cursor.execute("SELECT * FROM `lesson-team` WHERE team_id = %s ", team_id)
    myLessonPlan =dict_cursor.fetchall()
    if myLessonPlan:
        db.close()
        return jsonify(
            {
                "values": myLessonPlan,
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
            "errorMessage": "Invalid team",
            "message": None
        }
    )