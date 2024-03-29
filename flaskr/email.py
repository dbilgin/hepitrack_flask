import smtplib, ssl

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
from flask import current_app, jsonify

def send_email(email, data):
    if email=='test@hepitrack.com':
      return

    email_to=email
    email_from=current_app.config['SMTP_USER']

    smtp_server=current_app.config['SMTP_SERVER']
    smtp_user=current_app.config['SMTP_USER']
    smtp_pass=current_app.config['SMTP_PASS']

    msg=MIMEMultipart('alternative')
    msg['To']=email_to
    msg['From']=formataddr(
        (str(Header('Hepitrack', 'utf-8')), email_from)
    )
    msg['Subject']=data['subject']

    part=MIMEText(data['message'], 'html')

    msg.attach(part)

    s=smtplib.SMTP_SSL(smtp_server)
    s.login(smtp_user,smtp_pass)
    s.sendmail(email_from, email_to, msg.as_string())
    s.quit()

def email_verification_data(verification_token):
    subject='Email Verification'
    message="""\
      <img style="width: 60px; height: 60px;" src="https://hepitrack.web.app/images/logo.png"/>
      <div>You can verify your email address following the link below:</div>
      <div>
        <a href="https://hepitrack.web.app/verify-email.html?code=""" + verification_token + """">https://hepitrack.web.app/verify-email.html?code=""" + verification_token + """</a>
      </div>
      <div>Thanks for registering with Hepitrack!</<div>
    """
    return {
      'subject': subject,
      'message': message
    }

def email_reset_password(verification_token):
    subject='Email Verification'
    message="""\
      <img style="width: 60px; height: 60px;" src="https://hepitrack.web.app/images/logo.png"/>
      <div>Click the link below to reset your password:</div>
      <div>
        <a href="https://hepitrack.web.app/reset-password.html?code=""" + verification_token + """">https://hepitrack.web.app/reset-password.html?code=""" + verification_token + """</a>
      </div>
      <div>Thanks for using Hepitrack!</<div>
    """
    return {
      'subject': subject,
      'message': message
    }

def email_new_password(new_password):
    subject='New Password'
    message="""\
      <img style="width: 60px; height: 60px;" src="https://hepitrack.web.app/images/logo.png"/>
      <div>Your new password is as below:</div>
      <div>
        <b>""" + new_password + """</b>
      </div>
      <div>Thanks for using Hepitrack!</<div>
    """
    return {
      'subject': subject,
      'message': message
    }
