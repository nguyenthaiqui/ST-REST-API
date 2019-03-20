'''
@author: Evan, Kabaji
@version: 1.1
@since: Jan 19, 2019
'''
from flask import Flask, jsonify, request
import account
import distance
import exercise
import lesson
import record
import style
import team
import age
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
import datetime
from authentication import check_user

app = Flask(__name__)

# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = 'doan-xem'
jwt = JWTManager(app)


@app.route('/api/public/login', methods=['POST'])
# log in
def __signin__():
    return account.login(request.get_json())


@app.route('/api/public/register', methods=['POST'])
# register new account
def __signup__():
    return account.register(request.get_json())


@app.route('/api/public/forgotpassword/<email>/sendpin')
# send PIN to email for forgot password
def __send_PIN__(email):
    return account.send_email_to_change_password(email)


@app.route('/api/forgotpassword/<identity>/newpassword', methods=['POST'])
# forgot password, identity will be generated in __send_PIN__ function
@jwt_required
def __forgot_password__(identity):
    check_user(get_jwt_identity(), identity)
    return account.forgot_password(request.get_json())


@app.route('/api/<username>/createswimmer/<number>')
# auto create swimmer
@jwt_required
def __swimmer_creation__(number, username):
    check_user(get_jwt_identity(), username)
    return account.swimmer_creation(number, username)


@app.route('/api/<username>/deleteswimmeraccount/<swimmer_username>')
# delete a swimmer account, this function have some problems
@jwt_required
def __delete_swimmer_account__(username, swimmer_username):
    check_user(get_jwt_identity(), username)
    return account.delete_swimmer(username, swimmer_username)


@app.route('/api/profile/<username>/view')
# get all profile of user
@jwt_required
def __view_profile__(username):
    check_user(get_jwt_identity(), username)
    return account.get_info(username)


@app.route('/api/profile/<username>/edit', methods=['POST'])
# edit profile of user
@jwt_required
def __edit_profile__(username):
    check_user(get_jwt_identity(), username)
    return account.edit_info(username, request.get_json())


@app.route('/api/profile/<username>/changepassword', methods=['POST'])
# change password of an account
@jwt_required
def __change_password__(username):
    check_user(get_jwt_identity(), username)
    return account.change_password(username, request.get_json())


@app.route('/public/age', methods=['GET'])
def __get_age__():
    return age.get()


# request is a json must have keys(name,age)
@app.route('/team/<username>/add', methods=['POST'])
@jwt_required
def __add_team__(username):
    check_user(get_jwt_identity(), username)
    return team.add(username, request.get_json())


@app.route('/team/<username>/view')
@jwt_required
def __view_team__(username):
    check_user(get_jwt_identity(), username)
    return team.view(username)


@app.route('/team/<username>/<team_id>/edit', methods=['POST'])
@jwt_required
def __edit_team__(username, team_id):
    check_user(get_jwt_identity(), username)
    return team.edit(username, team_id, request.get_json())


@app.route('/team/<username>/<team_name>/add', methods=['POST'])
@jwt_required
def __add_swimmer__(username, team_name):
    check_user(get_jwt_identity(), username)
    return team.addSwimmer(team_name, request.get_json())


@app.route('/team/<username>/<team_id>/view')
@jwt_required
def __get_swimmer_info__(username, team_id):
    check_user(get_jwt_identity(), username)
    return team.getSwimmerInfo(team_id)


@app.route('/public/team/noteam')
def __get_swimmer_no_team__():
    return team.getSwimmerInfoNoTeam("No team")


@app.route('/team/<username>/<team_id>/add/<user_id>')
@jwt_required
def __add_swimmer_exit__(username, team_id, user_id):
    check_user(get_jwt_identity(), username)
    return team.addSwimmerExit(team_id, user_id)


@app.route('/team/<username>/<team_id>/delete')
@jwt_required
def __delete_team__(username, team_id):
    check_user(get_jwt_identity(), username)
    return team.delete(username, team_id)


@app.route('/team/<username>/<team_id>/delete/<id>')
@jwt_required
def __delete_swimmer__(username, team_id, id):
    check_user(get_jwt_identity(), username)
    return team.delSwimmer(team_id, id)


@app.route('/public/distance')
def __get_distance__():
    return distance.getDistance()

@app.route('/public/style')
def __get_style__():
    return style.getStyle()

@app.route('/public/type')
def __get_type_exercise():
    return exercise.getType()

@app.route('/team/<username>/<team_name>/record/add',methods=['POST'])
@jwt_required
def __add_record__(username,team_name):
    check_user(get_jwt_identity(),username)
    return record.addRecord(request.get_json())

@app.route('/workout/<username>/<team_id>/add',methods=['POST'])
def __add_lesson__(username,team_id):
    return lesson.add(request.get_json(), username, team_id)

@app.route('/workout/<username>/<team_id>/<lesson_id>/edit',methods=['POST'])
def __edit_lesson__(username,team_id,lesson_id):
    return lesson.edit(request.get_json(),username,team_id,lesson_id)
@app.route('/workout/<username>/<team_id>/<lesson_id>/delete')
def __delete_lesson__(username,team_id,lesson_id):
    return lesson.delete(lesson_id)

@app.route('/workout/<username>/<team_id>/<lesson_id>/add',methods=['POST'])
def __add_exercise__(username,team_id,lesson_id):
    return exercise.add(request.get_json(),lesson_id)



@app.route('/')
def __root__():
    return '<h1>Nắm bắt vận mệnh, khai phá thiên cơ</h1>'

# running web app in local machine
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
