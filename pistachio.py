#!/usr/bin/env python

"""
ARGS:
	-m selects a mailbox, does default action--shows messages from past week 
	-c configure email & password
	-m -s select a mailbox, search for a keyword in it
	-m -d select a mailbox, show messages since a specific date
	-f specify a flag (UNREAD, ETC.)
	-m -x select a mailbox, delete a specific message (done by id)
	--sh opens the shell, for multiple commands (So that initialize does not need to be run again)  
	No arg: view messages from past week in inbox 
"""
"""
	Shell commands:
	view [mailbox]: views a mailbox
	delete [id] deletes a message, throws an error if no mailbox is selected / id is invalid 
"""

import argparse 
import imaplib
import email
import getpass
import base64
import sys

def initialize():

	fname = "pist.conf"
	try: 
		if results.config:
			f = configure(fname)
		else:
			f = open(fname, 'r')
	except IOError:
		f = configure(fname)
	
	user = f.readline().strip("\n")
	password = base64.b64decode(f.readline().strip("\n"))
	
	MAIL_SERVERS = {'gmail.com': 'imap.gmail.com',
					'yahoo.com': 'imap.mail.yahoo.com',
					'aol.com': 'imap.aol.com'}
	
	user2 = user.split("@")
	if user2[1] not in MAIL_SERVERS:
		print "That server is not supported yet. Please enter another address"
		print "Upon trying again, add -c flag to reconfigure"
		sys.exit(1)

	else:
		IMAP_SERVER = imaplib.IMAP4_SSL(MAIL_SERVERS[user2[1]])
		IMAP_SERVER.login(user, password)

	return (IMAP_SERVER)
	
	 
def configure(fname):
	f = open(fname, 'w')
	print("CONFIGURING...")
	e = raw_input("Enter your email address ")

	while len(e.split("@")) != 2:
		e = raw_input("Enter your email address ")

	f.write(str(e + "\n"))
	f.write(base64.b64encode( getpass.getpass( "Enter your password (stored as base64 encoded str) " )))
	return f
	
def process_mailbox(IMAP_SERVER):
	#assume mailbox already selected
	mail_ids = get_mails_since_date(IMAP_SERVER)
	for id in mail_ids: 
		rv, data = IMAP_SERVER.fetch(id, 'RFC822')
		msg = email.message_from_string(data[0][1])

def get_mailboxes(IMAP_SERVER):
	mailboxes = IMAP_SERVER.list()	

def get_mails_since_date(IMAP_SERVER):
	#assume mailbox already selected
	months = {"01":"Jan", "02":"Feb", "03":"Mar", "04":"Apr", "05":"May", "06":"Jun", "07":"Jul", "08":"Aug", "09":"Sep", "10":"Oct", "11":"Nov", "12":"Dec"}

def get_mails_on_date(IMAP_SERVER):
	#assume mailbox already selected

def main():
	global results
	parser = argparse.ArgumentParser(description='Simple Terminal mail client')
	
	parser.add_argument("-m", action='store', dest='mailbox', help='Specify a mailbox', default="INBOX")
	parser.add_argument("-d", action='store', dest='date', help='Specify a date in the form of dd-mon-yyyy')
	parser.add_argument("-c", action='store_true', dest='config', help="change the username/password")
	parser.add_argument("-g", action='store', dest="mail_id", help="get a specific message based on its id", type=int)
	parser.add_argument("-s", action-'store', dest='keyword', help='search for a message in a mailbox based on a keyword', type=int)
	parser.add_argument("--od", action='store', dest="on_date", help="search for a message on a specific date, see -d for format")
	parser.add_argument("--sh", action="store_true", dest="act_shell", help="Add flag if you want to open shell", default=False)
	parser.add_argument("--lm", action="store_true", dest="list_mails", help="Add flag if you want to see the mailboxes in your account", default=False)

	results = parser.parse_args()
	
	IMAP_SERVER = initialize()
	

if __name__ == "__main__":
	main()
