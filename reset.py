from app import db, cursor

# resets test_register.py
email = "newemail@gmail.com"
name = "newname"
cursor.execute("DELETE FROM user WHERE email = %s AND name = %s", (email, name))

# resets test_manage_account.py
oldemail = "moezakbar@hotmail.com"
origpass = 1233
changedpass = 1234
cursor.execute("UPDATE user SET password = %s WHERE email = %s AND password = %s", (origpass, oldemail, changedpass))
db.commit()