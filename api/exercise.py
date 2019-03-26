'''
@author: Kabaji
@email: nguyenthaiqui233@gmail.com
@version: 1.0
@since: Mar 20, 2019
'''

import connector
from flask import jsonify

def getType():
    db, c = connector.connection()
    """get all databases from table exercise_type and convert to json"""
    c.execute("SELECT * FROM exercise_type")
    myTyle = c.fetchall()
    columns = ['id', 'type_name']
    # columns = [column[0] for column in c.description]        #get keys in db
    info = [dict(zip(columns, row)) for row in myTyle]  # create zip with key & value => convert dict
    db.close()
    return jsonify(info)

def addListExercise(data, lesson_id):
    db,c = connector.connection()
    dict_cursor = connector.getDictCursor()

    dict_cursor.execute("SELECT * FROM `lesson` WHERE id = %s",lesson_id)
    myLesson = dict_cursor.fetchone()

    if not myLesson:
        db.close()
        return jsonify(
            {
                "values": "",
                "success": False,
                "errorMessage": "Invalid lesson_id",
                "message": None
            }
        )
    for i in data:
        dict_cursor.execute("SELECT * FROM `exercise_type` WHERE id = %s", i['type_id'])
        myType = dict_cursor.fetchone()
        c.execute("SELECT * FROM `exercise` WHERE type_id = %s AND lesson_id = %s",(i['type_id'],lesson_id))
        if not c.fetchall():
            c.execute("INSERT INTO `exercise` (style_id,distance_id,repetition,description,type_id,lesson_id) VALUES(%s,%s,%s,%s,%s,%s)",
                      (i['style_id'],i['distance_id'],i['repetition'],i['description'],i['type_id'],lesson_id))
            db.commit()
        else:
            db.close()
            return jsonify(
                {
                    "values": "",
                    "success": False,
                    "errorMessage": "",
                    "message": None
                }
            )
    db.close()
    return jsonify(
        {
            "values": "added",
            "success": True,
            "errorMessage": "",
            "message": None
        }
    )
def view(lesson_id):
    db, c = connector.connection()
    dict_cursos = connector.getDictCursor()

    dict_cursos.execute("SELECT * FROM `exercise` WHERE lesson_id= %s", lesson_id)
    myExercise=dict_cursos.fetchall()
    return jsonify(
        [
            myExercise
        ]
    )