'''
@author: Evan
@email: lenguyenhoangvan18@gmail.com
@version: 1.0
@since: Mar 4, 2019
'''
import datetime


def check_user(current_user, username):
    if current_user != username:
        return jsonify(
            {
                "values": "Error",
                "success": False,
                "errorMessage": "Token authentication fail.",
                "message": None,
                "created_date": str(datetime.datetime.now())
            }
        )
