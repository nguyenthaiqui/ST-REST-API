'''
@author: Kabaji
@version: 1.0
@since: April 4, 2019
'''
from flask import jsonify

import connector
def addList(data):
    db,c = connector.connection()
    dict_cursor = connector.getDictCursor()

    result = []
    columns = ['diary_id', 'diary_date', 'rank']

    for user in data['swimmer']:
        dict_cursor.execute("SELECT * FROM `team-swimmer` WHERE user_id = %s AND team_id = %s",
                            (user['user_id'], data['team_id']))
        myUser = dict_cursor.fetchone()
        if myUser:
            dict_cursor.execute("SELECT * FROM `diary` WHERE user_id =%s AND lesson_id =%s",
                                (myUser['user_id'], data['lesson_id']))
            myDiary = dict_cursor.fetchone()
            if not myDiary:
                c.execute("INSERT INTO `diary` (user_id,team_id,lesson_id,date,note,rank_id) VALUES (%s,%s,%s,%s,%s,%s)",
                            (myUser['user_id'], data['team_id'], data['lesson_id'], data['date'], user['note'], user['rank_id']))
                db.commit()
            else:
                return jsonify(
                    {
                        "values": "",
                        "success": False,
                        "errorMessage": "Diary exits",
                        "message": None
                    }
                )
    c.execute("UPDATE `lesson-team` SET check_record = %s WHERE lesson_id = %s AND team_id = %s",(1,data['lesson_id'],data['team_id']))
    db.commit()

    return jsonify(
        {
            "values": "",
            "success": True,
            "errorMessage": "",
            "message": None
        }
    )


def add(data):
    '''POST json include keys (user_id,team_id,lesson_id,date,note,rank_id)'''
    db,c = connector.connection()
    dict_cursor = connector.getDictCursor()

    dict_cursor.execute("SELECT * FROM `team-swimmer` WHERE user_id = %s AND team_id = %s",(data['user_id'],data['team_id']))
    myUser = dict_cursor.fetchone()
    if myUser:
        dict_cursor.execute("SELECT * FROM `diary` WHERE user_id =%s AND lesson_id =%s",(myUser['id'],data['lesson_id']))
        myDiary = dict_cursor.fetchone()
        if not myDiary:
            c.execute("INSERT INTO `diary` (user_id,team_id,lesson_id,date,note,rank_id) VALUES (%s,%s,%s,%s,%s,%s)",
                      (myUser['id'],data['team_id'],data['lesson_id'],data['date'],data['note'],data['rank_id']))
            db.commit()
            c.close()
            db.close()
            dict_cursor.close()
            dict_cursor2 = connector.getDictCursor()
            dict_cursor2.execute("SELECT * FROM `diary` WHERE user_id = %s AND lesson_id = %s",
                                (myUser['id'], data['lesson_id']))
            mydiaryAdded = dict_cursor2.fetchone()
            dict_cursor2.execute("SELECT * FROM `rank` WHERE id = %s",mydiaryAdded['rank_id'])
            myRank = dict_cursor2.fetchone()
            dict_cursor2.close()
            return jsonify(
                {
                    "values":{
                        "rank": myRank['ranking'],
                        "diary_date": mydiaryAdded['date'].strftime("%Y-%m-%d"),
                        "diary_id":mydiaryAdded['id']
                    } ,

                    "success": True,
                    "errorMessage": "",
                    "message": None
                }
            )
        return jsonify(
            {
                "values": "",
                "success": False,
                "errorMessage": "Diary exits",
                "message": None
            }
        )
    return jsonify(
        {
            "values": "",
            "success": False,
            "errorMessage": "Invalid user",
            "message": None
        }
    )


def view(username):
    dict_cursor = connector.getDictCursor()
    dict_cursor.execute("SELECT * FROM user WHERE username = %s ",username)
    myCoach = dict_cursor.fetchone()

    dict_cursor.execute("SELECT DISTINCT  L.id AS lesson_id,L.name AS lesson_name, T.name AS team_name, D.date AS diary_date "
                        "FROM `lesson-team` LT, `team` T, `lesson` L, `diary` D "
                        "WHERE T.id = LT.team_id AND LT.lesson_id = L.id AND  D.lesson_id = L.id AND T.coach_id = %s AND LT.check_record = %s ",(myCoach['id'],1))
    myListResult = dict_cursor.fetchall()
    result = []
    columns = ['lesson_id','lesson_name', 'team_name', 'diary_date']
    for i in myListResult:
        listRow = [i['lesson_id'],i['lesson_name'],i['team_name'],i['diary_date'].strftime("%Y-%m-%d")]
        info = dict(zip(columns, listRow))
        result.append(info)
    dict_cursor.close()
    return jsonify(
        {
            "values": result,
            "success": True,
            "errorMessage": "",
            "message": None
        }
    )
def viewByDate(username,data):
    dict_cursor = connector.getDictCursor()
    dict_cursor.execute("SELECT * FROM user WHERE username = %s ", username)
    myCoach = dict_cursor.fetchone()

    dict_cursor.execute("SELECT DISTINCT  L.id AS lesson_id,L.name AS lesson_name, T.name AS team_name, D.date AS diary_date "
                        "FROM `lesson-team` LT, `team` T, `lesson` L, `diary` D "
                        "WHERE T.id = LT.team_id AND LT.lesson_id = L.id AND  D.lesson_id = L.id AND T.coach_id = %s AND LT.check_record = %s AND D.date = %s ",
                        (myCoach['id'], 1, data['diary_date']))
    myListResult = dict_cursor.fetchall()
    result = []
    columns = ['lesson_id','lesson_name', 'team_name']
    for i in myListResult:
        listRow = [i['lesson_id'],i['lesson_name'], i['team_name']]
        info = dict(zip(columns, listRow))
        result.append(info)
    dict_cursor.close()
    return jsonify(
        {
            "values": result,
            "success": True,
            "errorMessage": "",
            "message": None
        }
    )
def viewList(lesson_id):
    dict_cursor = connector.getDictCursor()
    dict_cursor.execute("SELECT U.first_name, U.last_name, R.ranking, D.note FROM `user` U, `rank` R, `diary` D WHERE U.id = D.user_id AND D.rank_id = R.id AND D.lesson_id = %s;",lesson_id)
    myListResult = dict_cursor.fetchall()
    result = []
    columns = ['first_name', 'last_name', 'rank','note']
    for i in myListResult:
        listRow = [i['first_name'], i['last_name'], i['ranking'],i['note']]
        info = dict(zip(columns, listRow))
        result.append(info)
    dict_cursor.close()
    return jsonify(
        {
            "values": result,
            "success": True,
            "errorMessage": "",
            "message": None
        }
    )

def edit(diary_id,data):
    '''POST json include keys (note, rank_id, heart_beat_id)'''
    db,c =connector.connection()
    dict_cursor = connector.getDictCursor()

    dict_cursor.execute("SELECT * FROM `diary` WHERE id = %s",diary_id)
    myDiary = dict_cursor.fetchone()
    if myDiary:
        c.execute("UPDATE `diary` SET note = %s, rank_id = %s, heart_beat_id=%s",
                  (data['note'],data['rank_id'],data['heart_beat_id']))
        db.commit()
        db.close()
        c.close()
        dict_cursor.close()
        dict_cursor2 = connector.getDictCursor()
        dict_cursor2.execute("SELECT * FROM `diary` WHERE id = %s",diary_id)
        myDiaryEdited = dict_cursor2.fetchone()
        return jsonify(
            {
                "values": myDiaryEdited,
                "success": True,
                "errorMessage": "",
                "message": None
            }
        )
    db.close()
    c.close()
    dict_cursor.close()
    return jsonify(
        {
            "values": "",
            "success": False,
            "errorMessage": "Invalid diary_id",
            "message": None
        }
    )