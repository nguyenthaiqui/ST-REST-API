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


def login(js_data):
	db = connector.connection()
	dict_cursor = connector.getDictCursor()
	try:
		dict_cursor.execute(
			'SELECT * FROM user WHERE username = %s', js_data['username'])
	except:
		return jsonify(
			{
				"values": "Error",
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
			js_data['password'].encode(), db_data['password'].encode())
		if db_data['password'].encode() == hashed_pw:
			# The next 4 lines is set up expires time
			expires = datetime.timedelta(
				seconds=constant.TOKEN_EXPIRES_TIME)
			access_token = create_access_token(
				identity=js_data['username'], expires_delta=expires)
			return jsonify(
				{
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
					"errorMessage": None,
					"message": "Accepted.",
					"created_date": str(datetime.datetime.now())
				}
			)
		else:
			return jsonify(
				{
					"values": "Error",
					"success": False,
					"errorMessage": "Authentication failed. Wrong password.",
					"message": None,
					"created_date": str(datetime.datetime.now())
				}
			)
	else:
		return jsonify(
			{
				"values": "Error",
				"success": False,
				"errorMessage": "User not found.",
				"message": None,
				"created_date": str(datetime.datetime.now())
			}
		)


def register(js_data):
	"""recive a new coach account json and return a status"""
	db, c = connector.connection()
	dict_cursor = connector.getDictCursor()
	dict_cursor.execute('SELECT username FROM user WHERE username = %s',
			  js_data['username'])
	db_data = dict_cursor.fetchone()
	if not db_data:  # create mew account
		hashed_pw = bcrypt.hashpw(
			js_data['password'].encode(), bcrypt.gensalt())  # hash password by bcrypt
		try:
			c.execute('''INSERT INTO 
						user (username, password, first_name, last_name, dob, gender,
						address, phone, email, role_id, is_verified, created_at)
						VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
					  (js_data['username'], hashed_pw, js_data['first_name'],
					   js_data['last_name'], js_data['dob'], js_data['gender'],
					   js_data['address'], js_data['phone'], js_data['email'],
					   1, 0, str(datetime.datetime.now())))
			db.commit()
		except:
			db.rollback()
			return jsonify(
				{
					"values": "Error",
					"success": False,
					"errorMessage": "Username already exists",
					"message": None,
					"created_date": str(datetime.datetime.now())
				}
			)
	dict_cursor.execute('SELECT id, password FROM user WHERE username = %s',
					  js_data['username'])
	db_data2 = dict_cursor.fetchone()
	return jsonify(
		{
			"values": {
				"user": {
					"id": db_data2['id'],
					"username": js_data['username'],
					"email": js_data['email'],
					"password": db_data2['password'],
					"first_name": js_data['first_name'],
					"last_name": js_data['last_name'],
					"dob": js_data['dob'],
					"role_id": 1				}
			},
			"success": True,
			"errorMessage": None,
			"message": "User Created",
			"created_date": str(datetime.datetime.now())
		}
	)



def swimmer_creation(number_of_swimmer, username):  # GET methods
	"""receive number of swimmer need to create"""
	db, c = connector.connection()
	dict_cursor = connector.getDictCursor()
	my_account_list = ""  # this string store account has been created
	i = 0
	while i < int(number_of_swimmer):
		rand_num = str(randint(1, 9999)).zfill(4)  # format 55 to 0055
		this_year = str(datetime.datetime.now().year)  # get this year
		randuser = 'st' + this_year + '_' + rand_num  # format st<this year>_<random number>
		dict_cursor.execute(
			'SELECT username FROM user WHERE username = %s', randuser)
		my_username = dict_cursor.fetchone()
		if not my_username:  # check duplication
			try:
				c.execute('''INSERT INTO user (username, password, 
							role_id, is_verified, created_at, dob)
							VALUES (%s, %s, %s, %s, %s, %s)''',
							(randuser, '1', 2, 0,
							str(datetime.datetime.now()), '2000-1-1'))
				# add account to string
				my_account_list += ('tai khoan: ' + randuser +
									'\n' + 'mat khau: ' + '1' + '\n' + '-' * 40 + '\n')
				db.commit()
			except:
				db.rollback()
				return jsonify(
					{
						"values": "Error",
						"success": False,
						"errorMessage": "Something went wrong.",
						"message": None,
						"created_date": str(datetime.datetime.now())
					}
				)
			i += 1
	# the next 4 lines store account to swimmer.txt
	f = open('swimmer.txt', 'w')
	temp = '-' * 40 + '\n' + my_account_list
	encoded = base64.b64encode(temp.encode())
	# encode before store in a text file
	f.write(str(encoded.decode()))
	return jsonify(
		{
			"values": number_of_swimmer + " swimmer created by " + username +".",
			"success": True,
			"errorMessage": None,
			"message": "Accepted.",
			"created_date": str(datetime.datetime.now())
		}
	)


def delete_swimmer(username, swimmer_username):
	"""just delete a swimmer by his/her username"""
	db, c = connector.connection()
	dict_cursor = connector.getDictCursor()
	try:
		c.execute('DELETE FROM user WHERE username = %s', swimmer_username)
		db.commit()
	except:
		db.rollback()
		return jsonify(
			{
				"values": "Error",
				"success": False,
				"errorMessage": "Something went wrong.",
				"message": None,
				"created_date": str(datetime.datetime.now())
			}
		)
	return jsonify(
		{
			"values": swimmer_username + " has been deleted by " + username +".",
			"success": True,
			"errorMessage": None,
			"message": "Accepted.",
			"created_date": str(datetime.datetime.now())
		}
	)


def get_info(username):
	"""return all information of a username"""
	db, c = connector.connection()
	dict_cursor = connector.getDictCursor()
	dict_cursor.execute('SELECT * FROM user WHERE username = %s', username)
	value = dict_cursor.fetchone()
	if not value:
		return jsonify(
			{
				"values": "Error",
				"success": False,
				"errorMessage": "No username like this.",
				"message": None,
				"created_date": str(datetime.datetime.now())
			}
		)
	return jsonify(
		{
			"values": {
				"user": value
			},
			"success": True,
			"errorMessage": None,
			"message": "Accepted.",
			"created_date": str(datetime.datetime.now())
		}
	)


def change_password(username, js_data):
	"""recive a json password and new password"""
	db, c = connector.connection()
	dict_cursor = connector.getDictCursor()
	dict_cursor.execute('SELECT password FROM user WHERE username = %s', username)
	my_password = dict_cursor.fetchone()
	hashed_pw = bcrypt.hashpw(
		js_data['password'].encode(), my_password['password'].encode())
	if my_password['password'].encode() == hashed_pw:
		try:
			c.execute('UPDATE user SET password = %s WHERE username = %s',
					  (bcrypt.hashpw(js_data['new_password'].encode(), bcrypt.gensalt()), username))
			db.commit()
			return jsonify(
				{
					"values": "Password of " + username + " has been changed.",
					"success": True,
					"errorMessage": None,
					"message": "Accepted.",
					"created_date": str(datetime.datetime.now())
				}
			)
		except:
			db.rollback()
	return jsonify(
				{
					"values": "Error",
					"success": False,
					"errorMessage": "Something went wrong.",
					"message": None,
					"created_date": str(datetime.datetime.now())
				}
			)


def edit_info(username, js_data):
	"""return success if edit success, else return fail"""
	db, c = connector.connection()
	dict_cursor = connector.getDictCursor()
	try:
		c.execute('''UPDATE user
					SET first_name = %s, last_name = %s, gender = %s, dob = %s, weight = %s,
						 height = %s, address = %s, phone = %s, email = %s, parent_name = %s,
						 parent_phone = %s
					WHERE username = %s''',
					(js_data['first_name'], js_data['last_name'], js_data['gender'],
					js_data['dob'], js_data['weight'], js_data['height'],
					js_data['address'], js_data['phone'], js_data['email'],
					js_data['parent_name'], js_data['parent_phone'], username))
		db.commit()
		return jsonify(
			{
				"values": "Profile of " + username + " has been changed.",
				"success": True,
				"errorMessage": None,
				"message": "Accepted.",
				"created_date": str(datetime.datetime.now())
			}
		)
	except:
		db.rollback()
	return jsonify(
		{
			"values": "Error",
			"success": False,
			"errorMessage": "Something went wrong.",
			"message": None,
			"created_date": str(datetime.datetime.now())
		}
	)