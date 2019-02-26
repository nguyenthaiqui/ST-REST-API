"""
@author : Kabaji
@version : 1.1
@since : 23 Jan 2019
"""
import base64

import connector
from flask import jsonify
import json
import JSONObject
import send_email

def add(username, data):
    """recieve json with key(name,age)
        return json key (result)"""
    db, c = connector.connection()
    c.execute("SELECT id FROM user WHERE username = %s", username)
    myData = c.fetchall()
    if myData:
        object_data = JSONObject.json2obj(json.dumps(data))
        c.execute("SELECT name FROM team WHERE coach_id = %s AND name = %s", (myData[0][0], object_data.team.name))
        if not c.fetchall():
            sql = "INSERT INTO team (coach_id,name,age) VALUES (%s, %s, %s)"
            value = (myData[0][0], object_data.team.name, object_data.team.age)
            c.execute(sql, value)
            db.commit()
            return jsonify({"result": "success"})
        return jsonify({"result": "team name exist"})
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
        object_data = JSONObject.json2obj(json.dumps(data))
        c.execute("SELECT name FROM team WHERE coach_id = %s AND name = %s", (myData[0][0], team_name))
        if c.fetchall():
            c.execute("UPDATE team SET name = %s, age =%s WHERE coach_id = %s AND name = %s",
                      (object_data.team.name, object_data.team.age, myData[0][0], team_name))
            db.commit()
            return jsonify({"result": "success"})
        return jsonify({"result": "not found"})
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


def addSwimmer(team_name,f):
    db, c = connector.connection()
    c.execute("SELECT id FROM team WHERE name =%s", team_name)
    myTeamID = c.fetchall()
    if myTeamID:
        '''decode file swimmer.txt'''
        temp = f.readline()
        a = temp.encode("UTF-8")
        decoded = base64.b64decode(a)
        temp2 = str(decoded, encoding="UTF-8")
        '''get id swimmer account and add to table `team-swimmer`'''
        s = temp2.split("----------------------------------------\n");
        i = 1;
        while (s[i] != ""):
            result = s[i].split()
            user = result[2]
            c.execute("SELECT id FROM user WHERE username = %s", user)
            myUserID = c.fetchall()
            if(myUserID):
                c.execute("INSERT INTO `team-swimmer`(user_id,team_id) VALUES(%s,%s)",(myUserID[0][0],myTeamID[0][0]))
                db.commit()
            i += 1
        return jsonify({"result": "success"})
    return jsonify({"result": "fail"})

def addSwimmerExit(team_name,user_id):
    db,c = connector.connection()
    c.execute("SELECT id FROM team WHERE name = %s",team_name)
    myTeamID = c.fetchall()
    if myTeamID:
        c.execute("UPDATE `team-swimmer` SET team_id = %s WHERE user_id")

def getIDSwimmer(team_name):
    db,c = connector.connection()
    c.execute("SELECT id FROM team WHERE name = %s ",team_name)
    myTeamID = c.fetchall()
    if myTeamID:
        c.execute("SELECT user_id FROM `team-swimmer` WHERE team_id = %s",myTeamID[0][0])
        mySwimmerID = c.fetchall()
        if mySwimmerID:
            columns = ['id']
            info = [dict(zip(columns, row)) for row in mySwimmerID]
            return jsonify({"team":info})
    return jsonify({"result":"fail"})

def delSwimmer(team_name,user_id):
    db,c = connector.connection()
    myTeamID = c.execute("SELECT id FROM team WHERE name = %s",team_name)
    if myTeamID:
        c.execute("UPDATE `team-swimmer` SET team_id = %s WHERE user_id= %s",(11,user_id))
        db.commit()
        return jsonify({"result":"success"})
    return jsonify({"result":"fail"})
