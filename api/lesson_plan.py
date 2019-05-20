'''
@author: Kabaji
@email: nguyenthaiqui233@gmail.com
@version: 1.0
@since: Mar 19, 2019
'''
import connector
from flask import jsonify
import datetime

def add(username,data):
    '''JSON include key : lesson_name,team_name,date'''
    db,c = connector.connection()
    dict_cursor = connector.getDictCursor()
    dict_cursor.execute("SELECT * FROM team where name = %s",data['team_name'])
    myTeam = dict_cursor.fetchone();
    dict_cursor.execute("SELECT * FROM lesson WHERE name = %s",data['lesson_name'])
    myLesson = dict_cursor.fetchone()
    dict_cursor.execute("SELECT * FROM `lesson-team` WHERE team_id = %s AND lesson_id = %s ",(myTeam['id'],myLesson['id']))
    if not dict_cursor.fetchone():
        c.execute("INSERT INTO `lesson-team` (lesson_id,team_id,date) VALUES (%s, %s, %s)",(myLesson['id'],myTeam['id'],data['date']))
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