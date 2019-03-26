'''
@author: Kabaji
@email: nguyenthaiqui233@gmail.com
@version: 1.0
@since: Mar 26, 2019
'''
from flask.json import jsonify

import connector


def add(username, data):
    '''json with key : user_id , team_id , date, note, rank_id, heart_beat_id'''
    db, c = connector.connection()
    dict_cursor = connector.getDictCursor()

    dict_cursor.execute("SELECT * FROM `diary` WHERE user_id = %s AND lesson_id = %s", (data['user_id'],data['lesson_id']))
    if not dict_cursor.fetchone():
        c.execute(
            "INSERT INTO `diary` (user_id, team_id, lesson_id, date, note, rank_id,heart_beat_id) VALUES (%s,%s,%s,%s,%s,%s,%s)",
            (data['user_id'],data['team_id'],data['lesson_id'],data['date'],data['note'],data['rank_id'],data['heart_beat_id'])
        )
        db.commit()
        db.close()
        return jsonify(
            {
                "values": "",
                "success": True,
                "errorMessage": "",
                "message": None,
            }
        )
    db.close()
    return jsonify(
        {
            "values": "Error",
            "success": False,
            "errorMessage": "Already add diary",
            "message": None,
        }
    )


def view(username, team_id):
    db, c = connector.connection()
    dict_cursor = connector.getDictCursor()

    dict_cursor.execute("SELECT * FROM `diary` WHERE team_id = %s", team_id)
    myDiary = dict_cursor.fetchall()
    db.close()
    if myDiary:
        return jsonify(myDiary)
    return jsonify(
        {
            "values": "Error",
            "success": False,
            "errorMessage": "Invalid team",
            "message": None,
        }
    )
