#!/usr/bin/env python

import cgi
import cgitb; cgitb.enable()  # for troubleshooting
import subprocess
import random
import string

print "Content-type: application/json"
print

prefix_saycel = "999100"
prefix_saycel2 = "999200"
prefix_rhizo =  "505051"

form = cgi.FieldStorage()
prefix = cgi.escape(form.getvalue("prefix", prefix_saycel))
email_address = cgi.escape(form.getvalue("email_address", ""))
if ";" in email_address:
  print """{ "status" : "err", "msg" : "email address contains semicolon, not supported, sorry" }"""
  exit()

if prefix != prefix_saycel and prefix != prefix_rhizo and prefix != prefix_saycel2:
  print """{ "status" : "err", "msg" : "wrong prefix, must be 999100, 999200 or 505051" }"""
else:
  for i in range(5):
    suffix = ''.join(random.choice(string.digits) for _ in range(5))
    username = prefix + suffix
    pwd = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))
    if subprocess.call(["/usr/sbin/kamctl", "add", username, pwd], stderr=subprocess.PIPE, stdout=subprocess.PIPE) == 0:
      if email_address != "":
	  subprocess.call(["/usr/sbin/kamctl", "sets", username, "email_address", email_address], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
      print """{ "status" : "ok", "msg" : "created user", "user" : "%s", "pwd" : "%s", "email_address" : "%s" }""" % (username, pwd, email_address)
      exit()
      
print """{ "status" : "err", "msg" : "could not create user, sorry" }"""
