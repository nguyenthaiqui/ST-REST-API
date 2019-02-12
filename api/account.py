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


def register(data):
    """recive a new coach account json and return a status"""
    db, c = connector.connection()
    obj_data = json2obj(dumps(data))
    c.execute('''SELECT username
                 FROM user
                 WHERE username = %s''', obj_data.coach.username)
    my_username = c.fetchall()
    if not my_username:  # create mew account
        try:
            c.execute('''INSERT INTO user (username, password, first_name, created_at, last_name,
                                           dob, gender, address, phone, email, role_id, is_verified)
                         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                      (obj_data.coach.username, obj_data.coach.password, obj_data.coach.first_name,
                       str(datetime.datetime.now()), obj_data.coach.last_name, obj_data.coach.dob, 
                       obj_data.coach.gender, obj_data.coach.address, obj_data.coach.phone, 
                       obj_data.coach.email, 1, 0))
            db.commit()
            return jsonify({'result': {'status': 'success'}})
        except:
            db.rollback()
    return jsonify({'result': {'status': 'fail'}})


def swimmer_creation(number_of_swimmer):
    db, c = connector.connection()
    my_account_list = ""
    for i in range(int(number_of_swimmer)):
        print(i)
        rand_num = str(randint(1000, 9999))
        this_year = str(datetime.datetime.now().year)  # get this year
        randuser = 'st' + this_year + '_' + rand_num
        c.execute('''SELECT username
                 FROM user
                 WHERE username = %s''', randuser)
        print(randuser)
        my_username = c.fetchall()
        print(my_username)
        if not my_username:
            try:
                c.execute('''INSERT INTO user (username, password, role_id, is_verified, created_at)
                             VALUES (%s, %s, %s, %s, %s)''',
                             (randuser, '1', 2, 0, str(datetime.datetime.now())))
                my_account_list += (randuser + '\n' + '1' + '\n' + '-'*40 + '\n')
                db.commit()
            except:
                db.rollback()
                return jsonify({'result': {'status': 'fail'}})
    f = open('swimmer.txt', 'w')
    f.write('-'*40 + '\n' + my_account_list)
    return jsonify({'result': {'status': 'success'}})


def delete_swimmer(data):
    pass


def login(data):
    """recive an account json and return login status"""
    db, c = connector.connection()
    obj_data = json2obj(dumps(data))
    c.execute('''SELECT username, password, id, role_id
                 FROM user
                 WHERE username = %s''', obj_data.user.username)
    my_data = c.fetchall()
    if my_data:
        if my_data[0][1] == obj_data.user.password:
            return jsonify({'result': {'status': 'success', 'id': my_data[0][2], 'role_id': my_data[0][3]}})
    return jsonify({'result': {'status': 'fail'}})


def get_info(username):
    """return all information of a username"""
    db, c = connector.connection()
    c.execute('''SELECT role_id, first_name, last_name, gender, dob, address,
                        phone, email, height, weight, parent_name, parent_phone
                 FROM user
                 WHERE username = %s''', username)
    value = c.fetchall()  # value is tuples
    if not value:
        return jsonify({'result': {'status': 'fail', 'notification': 'an error occurred'}})
    # this is key of json
    key_value_of_swimmer = ['role_id', 'first_name', 'last_name', 'gender', 'dob', 'address',
                            'phone', 'email', 'height', 'weight', 'parent_name', 'parent_phone']
    key_value_of_coach = ['role_id', 'first_name', 'last_name', 'gender',
                          'dob', 'address', 'phone', 'email']
    # store data in json with key is field name
    if value[0][0] == 1:  # value[0][0] is role_id
        # jsonify a key to a value
        return jsonify({"coach": dict(zip(key_value_of_coach, value[0]))})
    else:
        return jsonify({"swimmer": dict(zip(key_value_of_swimmer, value[0]))})


def change_password(username, data):
    """recive a json with username, password and the new one"""
    db, c = connector.connection()
    obj_data = json2obj(dumps(data))
    c.execute('''SELECT password
                 FROM user
                 WHERE username = %s''', username)
    my_password = c.fetchall()  # myPassword[0][0] is password
    if my_password[0][0] == obj_data.user.password and my_password[0][0] == obj_data.user.new_password:
        return jsonify({'status': 'fail', 'notification': 'new password must not same at the old one'})
    if my_password[0][0] == obj_data.user.password and my_password[0][0] != obj_data.user.new_password:
        try:
            c.execute('UPDATE user SET password = %s WHERE username = %s',
                      (obj_data.user.new_password, username))
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
    print(my_role[0][0])
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
