'''
@author: Kabaji
@version: 1.0
@since: April 4, 2019
'''
from flask import jsonify

import connector
def add(data):
    '''POST json include keys (username,team_id,lesson_id,date,note,rank_id)'''
    db,c = connector.connection()
    dict_cursor = connector.getDictCursor()

    dict_cursor.execute("SELECT * FROM `user` WHERE username = %s",data['username'])
    myUser = dict_cursor.fetchone()
    if myUser:
        dict_cursor.execute("SELECT * FROM `diary` WHERE user_id =%s AND lesson_id =%s",(myUser['id'],data['lesson_id']))
        myDiary = dict_cursor.fetchone()
        if not myDiary:
            c.execute("INSERT INTO `diary` (user_id,team_id,lesson_id,date,note,rank_id,heart_beat_id) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                      (myUser['id'],data['team_id'],data['lesson_id'],data['date'],data['note'],data['rank_id'],data['heart_beat_id']))
            db.commit()
            c.close()
            db.close()
            dict_cursor.close()
            dict_cursor2 = connector.getDictCursor()
            dict_cursor2.execute("SELECT * FROM `diary` WHERE user_id = %s AND lesson_id = %s",
                                (myUser['id'], data['lesson_id']))
            mydiaryAdded = dict_cursor2.fetchone()
            dict_cursor2.close()
            return jsonify(
                {
                    "values": mydiaryAdded,
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


def view(lesson_id):
    dict_cursor = connector.getDictCursor()

    dict_cursor.execute("SELECT * FROM `diary` WHERE lesson_id = %s",lesson_id)
    myListDiary = dict_cursor.fetchall()
    dict_cursor.close()
    return jsonify(
        {
            "values": myListDiary,
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