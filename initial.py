import sys 
import imaplib
import email
import datetime
import getpass

M = imaplib.IMAP4_SSL('imap.gmail.com')

try:
	M.login('hersh500@gmail.com', getpass.getpass())
except imaplib.IMAP4.error:
	sys.exit()

rv, data = M.select("INBOX")
if rv == "OK":
	rv, ids = M.search(None, "ALL","(SINCE 20-March-2015)")

for id in ids[0].split():
	rv, data = M.fetch(id, '(RFC822)')
	if rv != 'OK':
		print "ERROR"
		sys.exit()
	
	msg = email.message_from_string(data[0][1])
	print "Message %s: %s" % (id, msg['Subject'])
