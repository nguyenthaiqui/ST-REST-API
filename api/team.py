"""
@author : Kabaji
@version : 1.1
@since : 23 Jan 2019
"""

import connector
from flask import jsonify
import json
from collections import namedtuple




def add(username, data):
    """recieve json with key(name,age)
        return json key (result)"""
    db, c = connector.connection()
    c.execute("SELECT id FROM user WHERE username = %s", username)
    myData = c.fetchall()
    if myData:
        team = json.dumps(data)
        object_team = json.loads(team, object_hook=lambda d: namedtuple('TEAM', d.keys())(*d.values()))
        c.execute("SELECT name FROM team WHERE coach_id = %s AND name = %s", (myData[0][0],object_team.team.name))
        if not c.fetchall():
            sql = "INSERT INTO team (coach_id,name,age) VALUES (%s, %s, %s)"
            value = (myData[0][0], object_team.team.name, object_team.team.age)
            c.execute(sql, value)
            c.execute("SELECT id FROM team WHERE name = %s", object_team.team.name)
            myData2 = c.fetchall()
            sql2 = "INSERT INTO `team-swimmer` (user_id,team_id) VALUES(%s, %s)"
            value2 = (myData[0][0], myData2[0][0])
            c.execute(sql2, value2)
            db.commit()
            return jsonify({"result": "success"})
        return jsonify({"result":"team name exist"})
    return jsonify({"result": "fail"})


def view(username):
    """return list json with keys(id, coach_id, name, age)"""
    db, c = connector.connection()
    c.execute("SELECT id FROM user WHERE username = %s", username)
    myData = c.fetchall()
    if myData:
        c.execute("SELECT * FROM team WHERE coach_id = %s ", myData[0][0])
        myData2 = c.fetchall()
        columns = ['id', 'coach_id', 'name', 'age']
        info = [dict(zip(columns, row)) for row in myData2]
        return jsonify({"team": info})
    return jsonify({"result": "None"})


def edit(username, team_name, data):
    """recieve json with keys(name, age) return json with key(result)"""
    db, c = connector.connection()
    c.execute("SELECT id FROM user WHERE username = %s", username)
    myData = c.fetchall()
    if myData:
        team = json.dumps(data)
        object_team = json.loads(team, object_hook=lambda d: namedtuple('TEAM', d.keys())(*d.values()))
        c.execute("SELECT name FROM team WHERE coach_id = %s AND name = %s", (myData[0][0], team_name))
        if c.fetchall():
            team = json.dumps(data)
            object_team = json.loads(team, object_hook=lambda d: namedtuple('TEAM', d.keys())(*d.values()))
            c.execute("UPDATE team SET name = %s, age =%s WHERE coach_id = %s AND name = %s", (object_team.team.name, object_team.team.age, myData[0][0],team_name))
            db.commit()
            return jsonify({"result": "success"})
        return jsonify({"result":"not found"})
    return jsonify({"result": "fail"})


def delete(username, team_name):
    db, c = connector.connection()
    c.execute("SELECT id FROM user WHERE username = %s", username)
    myData = c.fetchall()
    if myData:
        c.execute("DELETE FROM team WHERE name = %s", team_name)
        db.commit()
        db.close()
        return jsonify({"result": "success"})
    return jsonify({"result": "fail"})



