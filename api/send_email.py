import smtplib
import decode_file
from flask import jsonify
from email6 import encoders
from email6.mime.text import MIMEText
from email6.mime.base import MIMEBase
from email6.mime.multipart import MIMEMultipart

def sendAttachment(data,filename):
    email_send = data['email']
    decode_file.decodeText('swimmer.txt', filename)

    """information"""
    email_user = 'wenmeah2@gmail.com'
    email_password = 'tinkendo'
    subject = 'Danh sách tài khoản của đội '

    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_send
    msg['Subject'] = subject
    body = " "
    try:
        """encode str utf-8"""
        msg.attach(MIMEText(body.encode('utf-8'), 'plain','utf-8'))

        attachment = open(filename, 'rb')

        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= " + filename)

        msg.attach(part)
        text = msg.as_string()
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_user, email_password)

        server.sendmail(email_user, email_send, text)
        server.quit()
        return jsonify({"result":"success"})
    except Exception as e:
        return jsonify({"result":"fail","Exception":e})


# # email_send = 'ntqui2303@gmail.com'
# def sendText(email_send):
#     email_user = 'wenmeah2@gmail.com'
#     email_password ='tinkendo'
#     subject = 'Python'
#     msg = MIMEMultipart()
#     msg['From'] = email_user
#     msg['To'] = email_send
#     msg['Subject'] = subject
#
#     body = 'Test'
#     msg.attach(MIMEText(body,'plain'))
#     text = msg.as_string()
#     server = smtplib.SMTP('smtp.gmail.com',587)
#     server.starttls()
#     server.login(email_user,email_password)
#
#     server.sendmail(email_user,email_send,text)
#     server.quit()
