#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
#############################
#                           #
# (C) 2016 by Alex Mirtoff  #
#                           #
# Рассылка всякого на почту #
#                           #
#############################
#

import smtplib
import sys
import time
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
from email.Utils import formatdate

def script_mail(script_date, script_all, script_new, script_addr, subj): 
    fromaddr = "robot@NAGIOS.***.ru"
    toaddr = "v.pon@****.net"
    admin = "mirtoff@*****.net"
     
    msg = MIMEMultipart()
 
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['CC'] = admin
    msg['Subject'] = "*** NAGIOS: " + subj
    msg['Date'] = formatdate(localtime = True)
    msg.set_charset("utf-8")
 
    body = '''Результат работы скрипта:
          
-----------------------------------------------

Дата: %s

Всего русскоязычных адресов: %s
Найдено русскоязычных новых адресов: %s

Адреса (если найдены):

%s

-----------------------------------------------


    ''' % (script_date, script_all, script_new, '\n'.join(script_addr))
 
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    server = smtplib.SMTP('mail.***.net', 25)
    text = msg.as_string()
    recipients = [toaddr, admin]
    server.sendmail(fromaddr, recipients, text)
    server.quit()
