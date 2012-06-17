#!/usr/bin/python

import cgitb
import cgi
import os

def createForm(text):
	return """
	<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/loose.dtd"><html>
	<html>
	<head>
	<title>RadioGaGa</title>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	</head>
	<body>
	<form method='post' accept-charset='utf-8'>
	%s
	<p><input type='submit' value='Formulardaten absenden'></p>
	</form>
	</body>
	</html>
	""" % (text,)

def formLine( ziffer, sender, info):
	return "<p>Sender Nr. %s: <input name='url%s' size='60' value='%s'>Info: <input name='info%s' size='60' value='%s'></p>\n" % ( ziffer, ziffer, sender, ziffer, info )

def formNew( zifferNew):
	return "<p>Sender Nr. %s: <input name='url%s' size='60'>Info: <input name='info%s' size='60'></p>\n" % (zifferNew, zifferNew, zifferNew)

cgitb.enable()
filename = "/var/www/channels.txt"
form = cgi.FieldStorage()
output = ""
FILE = open(filename,"r+")

if len(form) <= 0:
	# form empty
	zifferNew = 0
	text = ""

	for line in FILE:
		ziffer, sender, info  = line.split(";")
		zifferNew = int(ziffer)+1
		if str(ziffer) == "5":
			text += formLine( ziffer, sender, info.replace("\n", "")).replace("input", "input readonly") 
		else:
			text += formLine( ziffer, sender, info.replace("\n", "") )
	text += formNew(zifferNew)
	output += createForm(text)
else: 
	# form send
	toFile = ""
	text = ""
	output += "\n<p>Neue Senderliste gespeichert</p>\n"	
	for ziffer in range( 1, len(form)/2+1 ):
		urlID = "url%i" % (ziffer) 
		infoID = "info%i" % (ziffer)
		toFile += str(ziffer) + ";" + form[urlID].value + ";" + form[infoID].value + "\n"
		if str(ziffer) == "5":
			text += formLine( ziffer,form[urlID].value, form[infoID].value ).replace("input", "input readonly")
		else: 
			text += formLine( ziffer,form[urlID].value, form[infoID].value )
		zifferNew = ziffer+1
		
	FILE.write(toFile)
	FILE.close()
	text += formNew(zifferNew)	
	output += createForm(text)

# Required header that tells the browser how to render the text.
print "Content-Type: text/html\n\n"

# print html
print output
