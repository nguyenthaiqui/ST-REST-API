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

def add(data,lesson_id):
    db,c = connector.connection()
    dict_cursos = connector.getDictCursor()

    dict_cursos.execute("SELECT * FROM `lesson_plan` WHERE id = %s",lesson_id)
    myLesson = dict_cursos.fetchone()

    c.execute("SELECT * FROM `lesson_plan` WHERE id = %s",lesson_id)
    if not c.fetchall():
        db.close()
        return jsonify(
            {
                "values": "",
                "success": False,
                "errorMessage": "Invalid lesson_id",
                "message": None
            }
        )

    c.execute("SELECT * FROM `exercise` WHERE type = %s AND lesson_id = %s",(data['type_name'],lesson_id))
    if not c.fetchall():
        c.execute("INSERT INTO `exercise` (style,distance,repetition,description,type,lesson_id) VALUES(%s,%s,%s,%s,%s,%s)",
                  (data['swim_name'],data['swim_distance'],data['repetition'],data['description'],data['type_name'],lesson_id))
        db.commit()
        db.close()
        return jsonify(
            {
                "values": ""+ myLesson['name'] +" added "+ data['type_name'] + ": "+data['repetition']+"x"+data['swim_distance']+" "+data['swim_name'],
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
            "errorMessage": ""+ myLesson['name'] +" already have "+data['type_name'],
            "message": None
        }
    )
