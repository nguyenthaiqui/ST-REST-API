'''
@author: Evan, Kabaji
@version: 1.1
@since: Jan 19, 2019
'''
from flask import Flask, request
import account
import team
import age
app = Flask(__name__)


@app.route('/signin', methods=['POST'])
def __signin__():
    return account.login(request.get_json())


@app.route('/signup', methods=['POST'])
def __signup__():
    return account.register(request.get_json())


@app.route('/swimmergenerator/<number>')
def __swimmer_generator__(number):
	return account.swimmer_creation(number)


@app.route('/profile/<username>/view')
def __view_profile__(username):
    return account.get_info(username)


@app.route('/profile/<username>/edit', methods=['POST'])
def __edit_profile__(username):
    return account.edit_info(username, request.get_json())


@app.route('/profile/<username>/changepassword', methods=['POST'])
def __change_password__(username):
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
def __add_swimmer__(username,team_name):
    return team.addSwimmer(username,team_name,request.get_json()    )

@app.route('/team/<username>/<team_name>/delete')
def __delete_team__(username, team_name):
    return team.delete(username, team_name)

@app.route('/')
def __root__():
    return "DEPLOYED"


# running web app in local machine
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
