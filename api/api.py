'''
@author: Evan, Kabaji
@version: 1.1
@since: Jan 19, 2019
'''
from flask import Flask, jsonify, request
import account
import team
import age
import send_email
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
import datetime
from authentication import check_user

app = Flask(__name__)


# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = 'doan-xem'
jwt = JWTManager(app)


@app.route('/api/public/login', methods=['POST'])
def __signin__():
    return account.login(request.get_json())


@app.route('/api/public/register', methods=['POST'])
def __signup__():
    return account.register(request.get_json())


@app.route('/api/<username>/createswimmer/<number>')
@jwt_required
def __swimmer_creation__(number, username):
    check_user(get_jwt_identity(), username)
    return account.swimmer_creation(number, username)


@app.route('/api/<username>/deleteswimmeraccount/<swimmer_username>')
@jwt_required
def __delete_swimmer_account__(username, swimmer_username):
    check_user(get_jwt_identity(), username)
    return account.delete_swimmer(username, swimmer_username)


@app.route('/api/profile/<username>/view')
@jwt_required
def __view_profile__(username):
    check_user(get_jwt_identity(), username)
    return account.get_info(username)


@app.route('/api/profile/<username>/edit', methods=['POST'])
@jwt_required
def __edit_profile__(username):
    check_user(get_jwt_identity(), username)
    return account.edit_info(username, request.get_json())


@app.route('/api/profile/<username>/changepassword', methods=['POST'])
@jwt_required
def __change_password__(username):
    check_user(get_jwt_identity(), username)
    return account.change_password(username, request.get_json())


@app.route('/age', methods=['GET'])
def __get_age__():
    return age.get()


# request is a json must have keys(name,age)
@app.route('/team/<username>/add', methods=['POST'])
def __add_team__(username):
    return team.add(username, request.get_json())


@app.route('/team/<username>/view')
def __view_team__(username):
    return team.view(username)


@app.route('/team/<username>/<team_name>/edit', methods=['POST'])
def __edit_team__(username, team_name):
    return team.edit(username, team_name, request.get_json())


@app.route('/team/<username>/<team_name>/add', methods=['POST'])
def __add_swimmer__(team_name):
    f = open("swimmer.txt", "r")
    return team.addSwimmer(team_name, f)


@app.route('/team/<username>/<team_name>/view')
def __get_swimmer__(username, team_name):
    return team.getIDSwimmer(team_name)


@app.route('/team/noteam')
def __get_swimmer_no_team__():
    return team.getIDSwimmer("noteam")


@app.route('/team/<username>/<team_name>/delete')
def __delete_team__(username, team_name):
    return team.delete(username, team_name)


@app.route('/team/<username>/<team_name>/delete/<id>')
def __delete_swimmer__(username, team_name, id):
    return team.delSwimmer(team_name, id)


@app.route('/sendmail', methods=['POST'])
def __send_email__():
    return send_email.sendAttachment(request.get_json(), 'swimmer3.txt')


@app.route('/')
def __root__():
    return '<h1>Nắm bắt vận mệnh, khai phá thiên cơ</h1>'



# running web app in local machine
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
