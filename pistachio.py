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

def initialize():

	fname = "pist.conf"
	try: 
		if results.config:
			configure(fname)
		f = open(fname, 'r')
	except IOError:
		configure(fname)
		f = open(fname, 'r')
	
	user = f.readline().strip("\n")
	password = base64.b64decode(f.readline().strip("\n"))
	
	MAIL_SERVERS = {'gmail.com': 'imap.gmail.com',
					'yahoo.com': 'imap.mail.yahoo.com',
					'aol.com': 'imap.aol.com'}
	
	user2 = user.split("@")
	IMAP_SERVER = imaplib.IMAP4_SSL(MAIL_SERVERS[user2[1]])
	IMAP_SERVER.login(user, password)
	return (IMAP_SERVER)
	
	 
def configure(fname):
	f = open(fname, 'w')
	print("CONFIGURING...")
	e = raw_input("Enter your email address ")
	f.write(str(e + "\n"))
	f.write(base64.b64encode( getpass.getpass( "Enter your password (stored as base64 encoded str) " )))
	f.close()
	
def process_mailbox(IMAP_SERVER):

def main():
	global results
	parser = argparse.ArgumentParser(description='Simple Terminal mail client')
	
	parser.add_argument("-m", action='store', dest='mailbox', help='Specify a mailbox', default="INBOX")
	parser.add_argument("-d", action='store', dest='date', help='Specify a date in the form of dd-mon-yyyy')
	parser.add_argument("-c", action='store_true', dest='config', help="change the username/password")
	parser.add_argument("--sh", action="store_true", dest="act_shell", help="Add flag if you want to open shell", default=False)
	parser.add_argument("--lm", action="store_true", dest="list_mails", help="Add flag if you want to see the mailboxes in your account", default=False)

	results = parser.parse_args()
	
	IMAP_SERVER = initialize()
	

if __name__ == "__main__":
	main()
