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
    dict_cursor.close()
    c.close()
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
        print(type(myLessonPlan))
        dict_cursor.close()
        c.close()
        db.close()
        return jsonify(
            {
                "values": myLessonPlan,
                "success": True,
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
            "success": False,
            "errorMessage": "Invalid team",
            "message": None
        }
    )

def viewListLessonOfCoach(username):
    db,c = connector.connection()
    dict_cursor = connector.getDictCursor()

    dict_cursor.execute("SELECT * FROM user WHERE username = %s",username)
    myCoach = dict_cursor.fetchone();
    dict_cursor.execute("SELECT id,name FROM team WHERE coach_id = %s",myCoach['id'])
    myListTeam = dict_cursor.fetchall()
    result = []
    columns = ['lesson_id', 'team_name', 'lesson_name', 'date','check_record']
    for myTeam in myListTeam:
        dict_cursor.execute("SELECT L.id,L.name, DATE(LT.date) as date, LT.check_record FROM `lesson` L, `lesson-team` LT WHERE L.id = LT.lesson_id AND LT.team_id = %s ",myTeam['id'])
        myLesson = dict_cursor.fetchall()
        for lesson in myLesson:
            listRow = [lesson['id'],myTeam['name'],lesson['name'],lesson['date'].strftime("%Y-%m-%d"),lesson['check_record']]
            info = dict(zip(columns, listRow))
            result.append(info)
    dict_cursor.close()
    c.close()
    db.close()

    return jsonify(
        {
            "values": result,
            "success": True,
            "errorMessage": "",
            "message": None
        }
    )

def viewListLessonOfDate(username, data):
    db,c = connector.connection()
    dict_cursor = connector.getDictCursor()

    dict_cursor.execute("SELECT * FROM user WHERE username = %s",username)
    myCoach = dict_cursor.fetchone();
    dict_cursor.execute("SELECT id,name FROM team WHERE coach_id = %s",myCoach['id'])
    myListTeam = dict_cursor.fetchall()
    result = []
    columns = ['check_record','lesson_id', 'team_name', 'lesson_name']
    for myTeam in myListTeam:
        dict_cursor.execute("SELECT LT.check_record, L.id,L.name FROM `lesson` L, `lesson-team` LT WHERE L.id = LT.lesson_id AND LT.team_id = %s AND  LT.date= %s",(myTeam['id'],data['date']))
        myLesson = dict_cursor.fetchall()
        for lesson in myLesson:
            listRow = [lesson['check_record'],lesson['id'],myTeam['name'],lesson['name']]
            info = dict(zip(columns, listRow))
            result.append(info)
    dict_cursor.close()
    c.close()
    db.close()
    return jsonify(
        {
            "values": result,
            "success": True,
            "errorMessage": "",
            "message": None
        }
    )

def viewMember(username,data):
    db,c = connector.connection()
    dict_cursor = connector.getDictCursor()

    dict_cursor.execute("SELECT * FROM `team-swimmer` WHERE team_id = %s",data['team_id'])
