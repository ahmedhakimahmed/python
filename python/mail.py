import smtplib
s = smtplib.SMTP('localhost', 1025)
s.sendmail ('ahmed.hakimahmed@hotmail.com' ,'ahmed.abdelhakimahmed@hotmail.com', 'Hey buddy')
