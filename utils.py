# -*- coding: utf-8 -*-

import smtplib
import config
from email.mime.text import MIMEText

def send_mail(text):
    to_addr = config.TO_ADDR
    from_addr = config.FROM_ADDR
    mail_id = from_addr
    # 取得した16桁パスワードを入力する
    mail_pass = config.MAIL_PASS

    message = MIMEText('Hello')
    message['Subject'] = text
    message['From'] = from_addr
    message['To'] = to_addr

    sender = smtplib.SMTP_SSL('smtp.gmail.com')
    sender.login(mail_id, mail_pass)
    sender.sendmail(from_addr, to_addr, message.as_string())
    sender.quit()