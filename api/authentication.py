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
