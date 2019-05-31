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
    c.close()
    return jsonify(info)

def view(data):
    db,c = connector.connection()
    dict_cursor = connector.getDictCursor()
    dict_cursor.execute("SELECT * FROM lesson WHERE name = %s",data['lesson_name'])
    myLesson = dict_cursor.fetchone()
    dict_cursor.execute("SELECT  E.id as exercise_id,type_name,swim_name,swim_distance,repetition,description FROM exercise E,exercise_type ET, distance D,style S WHERE lesson_id = %s AND ET.id=E.type_id AND D.id = E.distance_id AND S.id = E.style_id",myLesson['id'])
    myExercise = dict_cursor.fetchall()
    return jsonify(
        {
        "lesson_id":myLesson['id'],
        "exercise":myExercise
        }
    )
