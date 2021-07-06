# -*- coding: utf-8 -*-

import smtplib
import os
from email.mime.text import MIMEText


def send_mail(title, text):
    to_addr = os.environ['TO_ADDR']
    from_addr = os.environ['FROM_ADDR']
    mail_id = from_addr
    # 取得した16桁パスワードを入力する
    mail_pass = os.environ['MAIL_PASS']

    message = MIMEText(text)
    message['Subject'] = title
    message['From'] = from_addr
    message['To'] = to_addr

    sender = smtplib.SMTP_SSL('smtp.gmail.com')
    sender.login(mail_id, mail_pass)
    sender.sendmail(from_addr, to_addr, message.as_string())
    sender.quit()


if __name__ == '__main__':
    send_mail("test")
