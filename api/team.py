'''
@author : Kabaji
@version : 1.1
@since : 23 Jan 2019
'''
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
            return jsonify(
                {
                    "values": "Team :"+ object_data.team.name + " has created",
                    "success": True,
                    "errorMessage": "",
                    "message": None
                }
            )
        return jsonify(
            {
                "values": "Error",
                "success": False,
                "errorMessage": "Team name exist",
                "message": None,
            }
        )
    return jsonify(
        {
            "values": "Error",
            "success": False,
            "errorMessage": "Invalid user",
            "message": None,
        }
    )


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
        return jsonify(
            {
                "values": {
                    "team":info
                },
                "success": True,
                "errorMessage": "",
                "message": None,
            }
        )
    else:
        return jsonify(
            {
                "values": "Error",
                "success": False,
                "errorMessage": "Invalid user",
                "message": None,
            }
        )
    return jsonify(
        {
            "values": "Error",
            "success": False,
            "errorMessage": "Empty",
            "message": None,
        }
    )


def edit(username,team_id, data):
    """recieve json with keys(name, age) return json with key(result)"""
    db, c = connector.connection()
    dict_cursor = connector.getDictCursor()
    dict_cursor.execute("SELECT id FROM user WHERE username = %s", username)
    myCoach = dict_cursor.fetchone()
    if myCoach:
        object_data = JSONObject.json2obj(json.dumps(data))
        dict_cursor.execute("SELECT * FROM `team` WHERE id = %s",team_id)
        myTeam = dict_cursor.fetchone()
        c.execute("SELECT name FROM team WHERE coach_id = %s AND name = %s", (myCoach['id'], myTeam['name']))
        if c.fetchall():
            c.execute("UPDATE team SET name = %s, age =%s WHERE coach_id = %s AND name = %s",
                      (object_data.team.name, object_data.team.age, myCoach['id'], myTeam['name']))
            db.commit()
            return jsonify(
                {
                    "values": ""+myTeam['name'] + " => " + object_data.team.name + ", "+myTeam['age']+" => "+ object_data.team.age,
                    "success": True,
                    "errorMessage": "",
                    "message": None,
                }
            )
        return jsonify(
            {
                "values": "Error",
                "success": False,
                "errorMessage": "Team doesn't exist.",
                "message": None,
            }
        )
    return jsonify(
        {
            "values": "Error",
            "success": False,
            "errorMessage": "Invalid user",
            "message": None,
        }
    )


def delete(username,team_id):
    db, c = connector.connection()
    dict_cursor = connector.getDictCursor()
    c.execute("SELECT id FROM user WHERE username = %s", username)
    myData = c.fetchall()
    if myData:
        dict_cursor.execute("SELECT * FROM `team` WHERE id = %s",team_id)
        myTeam = dict_cursor.fetchone()
        c.execute("DELETE FROM team WHERE id = %s", team_id)
        db.commit()
        db.close()
        return jsonify(
            {
                "values": "Team " + myTeam['name'] + " deleted. ",
                "success": True,
                "errorMessage": "",
                "message": None,
            }
        )
    return jsonify(
        {
            "values": "Error",
            "success": False,
            "errorMessage": "Invalid user",
            "message": None,
        }
    )


def addSwimmer(team_id, data):
    """Add swimmer account generated into DB"""
    db, c = connector.connection()
    dict_cursor = connector.getDictCursor()
    f = open("swimmer.txt", "r")
    dict_cursor.execute("SELECT * FROM team WHERE id = %s",team_id)
    myTeam = dict_cursor.fetchone()
    if myTeam:
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
            dict_cursor.execute("SELECT * FROM user WHERE username = %s",user)
            mySwimmer = dict_cursor.fetchone()
            # c.execute("SELECT id FROM user WHERE username = %s", user)
            # myUserID = c.fetchall()
            if (mySwimmer):
                c.execute("SELECT user_id FROM `team-swimmer` WHERE user_id = %s", mySwimmer['id'])
                if not c.fetchall():
                    c.execute("INSERT INTO `team-swimmer`(user_id,team_id) VALUES(%s,%s)",
                              (mySwimmer['id'], myTeam['id']))
                    db.commit()
            i += 1
        return send_email.sendAttachment(data, 'swimmer3.txt')
    return jsonify(
        {
            "values": "Error",
            "success": False,
            "errorMessage": "Invalid team",
            "message": None,
        }
    )


def addSwimmerExit(team_id, user_id):
    db, c = connector.connection()
    dict_cursor = connector.getDictCursor()
    dict_cursor.execute("SELECT * FROM `user` WHERE id = %s",user_id)
    mySwimmer = dict_cursor.fetchone()
    dict_cursor.execute("SELECT * FROM `team` WHERE id = %s",team_id)
    myTeam = dict_cursor.fetchone()
    if myTeam:
        c.execute("UPDATE `team-swimmer` SET team_id = %s WHERE user_id = %s", (myTeam['id'], user_id))
        db.commit()
        return jsonify(
            {
                "values":  mySwimmer['username'] + " added into team : " + myTeam['name'],
                "success": True,
                "errorMessage": "",
                "message": None,
            }
        )
    return jsonify(
        {
            "values": "Error",
            "success": False,
            "errorMessage": "Invalid user_id",
            "message": None,
        }
    )

def getSwimmerInfo(team_id):
    db, c = connector.connection()
    dict_cursor = connector.getDictCursor()
    dict_cursor.execute("SELECT * FROM `team` WHERE id = %s",team_id)
    myTeam = dict_cursor.fetchone()
    if myTeam:
        c.execute("SELECT user_id FROM `team-swimmer` WHERE team_id = %s", myTeam['id'])
        mySwimmerID = c.fetchall()
        result = []
        columns = ['id','username','dob' ,'first_name', 'last_name']
        for row in mySwimmerID:
            dict_cursor.execute("SELECT username,dob,first_name,last_name FROM `user` WHERE id = %s", row[0])
            mySwimmerInfo = dict_cursor.fetchone()
            listRow = [row[0],mySwimmerInfo['username'],mySwimmerInfo['dob'], mySwimmerInfo['first_name'], mySwimmerInfo['last_name']]
            info = dict(zip(columns, listRow))
            result.append(info)
        return jsonify(
            {
                "values": {
                    "team":result
                },
                "success": True,
                "errorMessage": "",
                "message": None,
            }
        )
    return jsonify(
        {
            "values": "Error",
            "success": False,
            "errorMessage": "Invalid team",
            "message": None,
        }
    )

def getSwimmerInfoNoTeam(team_name):
    db, c = connector.connection()
    dict_cursor = connector.getDictCursor()
    dict_cursor.execute("SELECT * FROM `team` WHERE name = %s", team_name)
    myTeam = dict_cursor.fetchone()
    if myTeam:
        c.execute("SELECT user_id FROM `team-swimmer` WHERE team_id = %s", myTeam['id'])
        mySwimmerID = c.fetchall()
        result = []
        columns = ['id', 'username', 'dob', 'first_name', 'last_name']
        for row in mySwimmerID:
            dict_cursor.execute("SELECT username,dob,first_name,last_name FROM `user` WHERE id = %s", row[0])
            mySwimmerInfo = dict_cursor.fetchone()
            listRow = [row[0], mySwimmerInfo['username'], mySwimmerInfo['dob'], mySwimmerInfo['first_name'],
                       mySwimmerInfo['last_name']]
            info = dict(zip(columns, listRow))
            result.append(info)
        return jsonify(
            {
                "values": {
                    "team": result
                },
                "success": True,
                "errorMessage": "",
                "message": None,
            }
        )
    return jsonify(
        {
            "values": "Error",
            "success": False,
            "errorMessage": "Invalid team",
            "message": None,
        }
    )

def delSwimmer(team_id, user_id):
    db, c = connector.connection()
    dict_cursor = connector.getDictCursor()
    dict_cursor.execute("SELECT * FROM team WHERE id = %s",team_id)
    myTeam = dict_cursor.fetchone()
    if myTeam:
        dict_cursor.execute("SELECT * FROM `user` WHERE id = %s", user_id)
        mySwimmer = dict_cursor.fetchone()
        if mySwimmer:
            dict_cursor.execute("SELECT id FROM team where name = %s", "No team")
            myNoTeam = dict_cursor.fetchone()
            c.execute("UPDATE `team-swimmer` SET team_id = %s WHERE user_id= %s", (myNoTeam['id'], user_id))
            db.commit()
            return jsonify(
                {
                    "values": mySwimmer['username'] + " in team " + myTeam['name'] + " deleted.",
                    "success": True,
                    "errorMessage": "",
                    "message": None,
                }
            )
        return jsonify(
            {
                "values": "Error",
                "success": False,
                "errorMessage": "Invalid user_id",
                "message": None,
            }
        )
    return jsonify(
        {
            "values": "Error",
            "success": False,
            "errorMessage": "Invalid team",
            "message": None,
        }
    )
