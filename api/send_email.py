'''
@author: Kabaji
@email: nguyenthaiqui233@gmail.com
@version: 1.0
@since: Feb 26, 2019
'''

import smtplib
import decode_file
from flask import jsonify
from email6 import encoders
from email6.mime.text import MIMEText
from email6.mime.base import MIMEBase
from email6.mime.multipart import MIMEMultipart


def sendAttachment(data, filename):
    email_send = data['email']
    decode_file.decodeText('swimmer.txt', filename)

    """information"""
    email_user = 'swimtracker001@gmail.com'
    email_password = 'dinhluu123'
    subject = '[SwimTracker] Danh sách tài khoản của đội '

    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_send
    msg['Subject'] = subject
    body = " "
    try:
        """encode str utf-8"""
        msg.attach(MIMEText(body.encode('utf-8'), 'plain', 'utf-8'))

        attachment = open(filename, 'rb')

        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        "attachment; filename= " + filename)

        msg.attach(part)
        text = msg.as_string()
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_user, email_password)

        server.sendmail(email_user, email_send, text)
        server.quit()
        return jsonify(
            {
                "values": "The list of swimmer account has sent to email : "+data['email'],
                "success": True,
                "errorMessage": "",
                "message": None,
            }
        )
    except Exception as e:
        return jsonify(
            {
                "values": "Error",
                "success": False,
                "errorMessage": e,
                "message": None,
            }
        )


def sendText(email_send, last_name, reset_password_token):
    email_user = 'swimtracker001@gmail.com'
    email_password = 'dinhluu123'
    subject = '[SwimTracker] Thay đổi mật khẩu'
    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_send
    msg['Subject'] = subject

    body = 'Chào ' + last_name +', \n'
    body += 'Chúng tôi vừa nhận được yêu cầu thay đổi mật khẩu của bạn từ SwimTracker.\n\n'
    body += 'Mã PIN: ' + reset_password_token + '\n\n'
    body += 'Nếu bạn không yêu cầu thay đổi mật khẩu, làm ơn bỏ qua tin nhắn này hoặc\n'
    body += 'trả lời cho chúng tôi biết. Mã PIN sẽ chỉ tồn tại trong 30 phút.\n'
    body += 'Chân thành cám ơn!\n'
    body += 'SwimTracker Develope Team'
    msg.attach(MIMEText(body.encode('utf-8'), 'plain', 'utf-8'))
    text = msg.as_string()
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_user, email_password)

    server.sendmail(email_user, email_send, text)
    server.quit()
