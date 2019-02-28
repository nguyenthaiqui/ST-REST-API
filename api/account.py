'''
@author: Evan
@email: lenguyenhoangvan18@gmail.com
@version: 1.0
@since: Jan 19, 2019
'''
import connector
from flask import jsonify
from JSONObject import json2obj  # json2obj recive a string
from json import dumps
from random import randint
import datetime
import base64
import bcrypt
from flask_jwt_extended import create_access_token
import constant


def login(data):
    db = connector.connection()
    dict_cursor = connector.getDictCursor()
    try:
        dict_cursor.execute(
            'SELECT * FROM user WHERE username = %s', data['username'])
    except:
        return jsonify(
            {
                "value": "Error",
                "values": [],
                "total": 1,
                "success": False,
                "errorMessage": "Invalid user.",
                "message": None,
                "created_date": str(datetime.datetime.now())
            }
        )
    db_data = dict_cursor.fetchone()
    if db_data:
        # The next 3 lines check hashed password is valid for login
        hashed_pw = bcrypt.hashpw(
            data['password'].encode(), db_data['password'].encode())
        if db_data['password'].encode() == hashed_pw:
            # The next 4 lines is set up expires time
            expires = datetime.timedelta(
                seconds=constant.TOKEN_EXPIRES_TIME)
            access_token = create_access_token(
                identity=data['username'], expires_delta=expires)
            return jsonify(
                {
                    "value": {},
                    "values": {
                        "token": access_token,
                        "expiresIn": constant.TOKEN_EXPIRES_TIME,
                        "user": {
                            "username": db_data['username'],
                            "role_id": db_data['role_id'],
                            "first_name": db_data['first_name'],
                            "last_name": db_data['last_name'],
                            "dob": db_data['dob'],
                            "phone": db_data['phone'],
                            "email": db_data['email'],
                            "address": db_data['address'],
                            "parent_name": db_data['parent_name'],
                            "parent_phone": db_data['parent_phone'],
                            "gender": db_data['gender'],
                            "is_verified": db_data['is_verified'],
                            "age": db_data['age'],
                            "height": db_data['height'],
                            "weight": db_data['weight'],
                            "avatar": db_data['avatar'],
                            "slug": db_data['slug'],
                            "created_at": db_data['created_at'],
                            "updated_at": db_data['updated_at']
                        }
                    },
                    "success": True,
                    "errorMessage": "",
                    "message": "Accepted",
                    "created_date": str(datetime.datetime.now())
                }
            )
        else:
            return jsonify(
                {
                    "value": "Error",
                    "values": [],
                    "total": 1,
                    "success": False,
                    "errorMessage": "Authentication failed. Wrong password.",
                    "message": None,
                    "created_date": str(datetime.datetime.now())
                }
            )
    else:
        return jsonify(
            {
                "value": "Error",
                "values": [],
                "total": 1,
                "success": False,
                "errorMessage": "User not found.",
                "message": None,
                "created_date": str(datetime.datetime.now())
            }
        )


def register(data):
    """recive a new coach account json and return a status"""
    db, c = connector.connection()
    obj_data = json2obj(dumps(data))
    c.execute('''SELECT username
                 FROM user
                 WHERE username = %s''', obj_data.coach.username)
    my_username = c.fetchall()
    if not my_username:  # create mew account
        hashed_pw = bcrypt.hashpw(
            obj_data.coach.password.encode(), bcrypt.gensalt())  # hash password by bcrypt
        try:
            c.execute('''INSERT INTO user (username, password, first_name, created_at, last_name,
                                           dob, gender, address, phone, email, role_id, is_verified)
                         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                      (obj_data.coach.username, hashed_pw, obj_data.coach.first_name,
                       str(datetime.datetime.now()
                           ), obj_data.coach.last_name, obj_data.coach.dob,
                       obj_data.coach.gender, obj_data.coach.address, obj_data.coach.phone,
                       obj_data.coach.email, 1, 0))
            db.commit()
            return jsonify({'result': {'status': 'success'}})
        except:
            db.rollback()
    return jsonify({'result': {'status': 'fail'}})


def swimmer_creation(number_of_swimmer):
    """receive number of swimmer need to create"""
    db, c = connector.connection()
    my_account_list = ""  # this string store account has been created
    i = 0
    while i < int(number_of_swimmer):
        rand_num = str(randint(1, 9999)).zfill(4)  # format 55 to 0055
        this_year = str(datetime.datetime.now().year)  # get this year
        randuser = 'st' + this_year + '_' + rand_num  # format st<year>_<random number>
        c.execute('''SELECT username
                 FROM user
                 WHERE username = %s''', randuser)
        my_username = c.fetchall()
        if not my_username:  # check duplication
            try:
                c.execute('''INSERT INTO user (username, password, role_id, is_verified, created_at, dob)
                             VALUES (%s, %s, %s, %s, %s, %s)''',
                          (randuser, '1', 2, 0, str(datetime.datetime.now()), '2000-1-1'))
                my_account_list += ('tai khoan: ' + randuser +
                                    '\n' + 'mat khau: ' + '1' + '\n' + '-' * 40 + '\n')  # add account to string
                db.commit()
            except:
                db.rollback()
                return jsonify({'result': {'status': 'fail'}})
            i += 1
    f = open('swimmer.txt', 'w')
    temp = '-' * 40 + '\n' + my_account_list
    encoded = base64.b64encode(temp.encode())
    f.write(str(encoded.decode()))  # encode before store in a text file
    return jsonify({'result': {'status': 'success'}})


def delete_swimmer(username):
    """just delete a swimmer by his/her username"""
    db, c = connector.connection()
    try:
        c.execute('''DELETE FROM user
                     WHERE username = %s''', username)
        db.commit()
    except:
        db.rollback()
        return jsonify({'result': {'status': 'fail'}})
    return jsonify({'result': {'status': 'success'}})


def get_info(username):
    """return all information of a username"""
    db, c = connector.connection()
    c.execute('''SELECT id, role_id, first_name, last_name, gender, dob, address,
                        phone, email, height, weight, parent_name, parent_phone
                 FROM user
                 WHERE username = %s''', username)
    value = c.fetchall()  # value is tuples
    if not value:
        return jsonify({'result': {'status': 'fail', 'notification': 'an error occurred'}})
    # this is key of json
    key_value = ['id', 'role_id', 'first_name', 'last_name', 'gender', 'dob', 'address',
                 'phone', 'email', 'height', 'weight', 'parent_name', 'parent_phone']
    # jsonify a key to a value
    return jsonify({"user": dict(zip(key_value, value[0]))})


def change_password(username, data):
    """recive a json password and new password"""
    db, c = connector.connection()
    obj_data = json2obj(dumps(data))
    c.execute('''SELECT password
                 FROM user
                 WHERE username = %s''', username)
    my_password = c.fetchall()  # myPassword[0][0] is password
    hashed_pw = bcrypt.hashpw(
        obj_data.user.password.encode(), my_password[0][0].encode())
    if my_password[0][0].encode() == hashed_pw:
        try:
            c.execute('UPDATE user SET password = %s WHERE username = %s',
                      (bcrypt.hashpw(obj_data.user.new_password.encode(), bcrypt.gensalt()), username))
            db.commit()
            return jsonify({'result': {'status': 'success'}})
        except:
            db.rollback()
    return jsonify({'result': {'status': 'fail'}})


def edit_info(username, data):
    """return success if edit success, else return fail"""
    db, c = connector.connection()
    obj_data = json2obj(dumps(data))
    c.execute('SELECT role_id FROM user WHERE username = %s', username)
    my_role = c.fetchall()
    if my_role[0][0] == 1:
        try:
            c.execute('''UPDATE user
                         SET first_name= %s, last_name = %s, gender = %s, dob = %s,
                             address = %s, phone = %s, email = %s
                         WHERE username = %s''',
                      (obj_data.coach.first_name, obj_data.coach.last_name, obj_data.coach.gender,
                       obj_data.coach.dob, obj_data.coach.address, obj_data.coach.phone,
                       obj_data.coach.email, username))
            db.commit()
            return jsonify({'result': {'status': 'success'}})
        except:
            db.rollback()
    else:
        try:
            c.execute('''UPDATE user
                         SET first_name= %s, last_name = %s, gender = %s, dob = %s, weight = %s,
                             height = %s, address = %s, phone = %s, email = %s, parent_name = %s,
                             parent_phone = %s
                         WHERE username = %s''',
                      (obj_data.swimmer.first_name, obj_data.swimmer.last_name, obj_data.swimmer.gender,
                       obj_data.swimmer.dob, obj_data.swimmer.weight, obj_data.swimmer.height,
                       obj_data.swimmer.address, obj_data.swimmer.phone, obj_data.swimmer.email,
                       obj_data.swimmer.parent_name, obj_data.swimmer.parent_phone, username))
            db.commit()
            return jsonify({'result': {'status': 'success'}})
        except:
            db.rollback()
    return jsonify({'result': {'status': 'fail'}})
