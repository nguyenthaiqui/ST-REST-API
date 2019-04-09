'''
@author: Evan, Kabaji
@version: 1.1
@since: Jan 19, 2019
'''
from flask import Flask, jsonify, request
import account
import diary
import distance
import exercise
import heart_beat
import lesson
import rank
import record
import style
import team
import age
import lesson_plan
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
    return account.swimmer_creation(number)


@app.route('/api/<username>/addswimmer', methods=['POST'])
# add swimmer to db
@jwt_required
def __swimmer_add__(username):
    check_user(get_jwt_identity(), username)
    return account.swimmer_add(request.get_json())


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


@app.route('/team/<username>/add/<user_id>', methods=['POST'])
@jwt_required
def __add_swimmer_exit__(username, user_id):
    check_user(get_jwt_identity(), username)
    return team.addSwimmerExit(user_id, request.get_json())


@app.route('/team/<username>/<team_id>/delete')
@jwt_required
def __delete_team__(username, team_id):
    check_user(get_jwt_identity(), username)
    return team.delete(username, team_id)


@app.route('/team/<username>/<team_id>/delete/<user_id>')
@jwt_required
def __delete_swimmer__(username, team_id, user_id):
    check_user(get_jwt_identity(), username)
    return team.delSwimmer(team_id, user_id)


@app.route('/public/age', methods=['GET'])
def __get_age__():
    return age.get()


@app.route('/public/team/noteam')
def __get_swimmer_no_team__():
    return team.getSwimmerInfoNoTeam("No team")


@app.route('/public/distance')
def __get_distance__():
    return distance.getDistance()


@app.route('/public/style')
def __get_style__():
    return style.getStyle()


@app.route('/public/type')
def __get_type_exercise__():
    return exercise.getType()


@app.route('/public/heartbeat')
def __get_heart_beat__():
    return heart_beat.getHeartBeat()


@app.route('/public/rank')
def __get_rank__():
    return rank.getRank()


@app.route('/workout/<username>/lesson/add', methods=['POST'])
def __add_lesson__(username):
    return lesson.add(request.get_json(), username)


@app.route('/workout/<username>/lesson/view')
def __view_lesson__(username):
    return lesson.view(username)


@app.route('/workout/<username>/lesson/edit/<lesson_id>', methods=['POST'])
def __edit_lesson__(username, lesson_id):
    return lesson.edit(request.get_json(), username, lesson_id)


@app.route('/workout/<username>/lesson/delete/<lesson_id>')
def __delete_lesson__(username, lesson_id):
    return lesson.delete(lesson_id)


@app.route('/workout/<username>/lessonplan/add/<lesson_id>/<team_id>', methods=['POST'])
def __add_lesson_plan__(username, lesson_id, team_id):
    return lesson_plan.add(username, lesson_id, team_id, request.get_json())


@app.route('/workout/<username>/lessonplan/view/<team_id>')
def __view_lesson_plan__(username, team_id):
    return lesson_plan.view(team_id)


@app.route('/record/<username>/add', methods=['POST'])
def __add_record__(username):
    return record.add(username, request.get_json())


@app.route('/diary/<username>/add', methods=['POST'])
# POST json include keys (username,team_id,lesson_id,date,note,rank_id)
def __add_diary__(username):
    return diary.add(request.get_json())


@app.route('/diary/<username>/view/<lesson_id>')
def __view_diary__(username, lesson_id):
    return diary.view(lesson_id)


@app.route('/diary/<username>/edit/<diary_id>', methods=['POST'])
# recieve json with keys(name, age) return json with key(result)
def __edit_diary__(username, diary_id):
    return diary.edit(diary_id, request.get_json())


@app.route('/')
def __root__():
    return '<h1>Nắm bắt vận mệnh, khai phá thiên cơ</h1>'


# running web app in local machine
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
