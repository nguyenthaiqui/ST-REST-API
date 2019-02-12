'''
@author: Evan, Kabaji
@version: 1.1
@since: Jan 19, 2019
'''
from flask import Flask, request
import account

app = Flask(__name__)


@app.route('/signin', methods=['POST'])
def __signin__():
    return account.login(request.get_json())


@app.route('/signup', methods=['POST'])
def __signup__():
    return account.register(request.get_json())


@app.route('/createswimmer/<number>')
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


@app.route('/')
def __root__():
    return "DEPLOYED"


# running web app in local machine
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
