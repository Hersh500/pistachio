#!/usr/bin/env python
#HERSH SANGHVI
#TODO: Add support for RFC search flags that require keywords https://tools.ietf.org/html/rfc3501#section-6.4.4

"""
ARGS:
	-m selects a mailbox, does default action--shows messages from past week 
	-c configure email & password
	-m -s select a mailbox, search for a keyword in it
	-m -d select a mailbox, show messages since a specific date
	-f specify a flag (UNREAD, ETC.)
	-m -x select a mailbox, delete a specific message (by id)
	No arg: view messages from past week in inbox 
"""

__version__ = "1.0.0"

import argparse 
import imaplib
import email
import getpass
import base64
import sys
import datetime
import os
from .dehtml import dehtml 

def initialize():

	fname = "/Users/" + getpass.getuser() + "/.pistrc"

	try: 
		if results.config:
			f = _configure(fname)
		else:
			os.chdir("/Users/" + getpass.getuser())
			f = open(fname, 'r')
	except IOError:
		_configure(fname)
		f = open(fname, 'r')
	
	user = f.readline().strip("\n")
	password = base64.b64decode(f.readline().strip("\n"))
	
	MAIL_SERVERS = {'gmail.com': 'imap.gmail.com',
					'yahoo.com': 'imap.mail.yahoo.com',
					'aol.com': 'imap.aol.com'}
	
	user2 = user.split("@")
	if user2[1] not in MAIL_SERVERS:
		print "That server is not supported yet. Please enter another address"
		print "add -c flag to reconfigure"
		sys.exit(1)

	else:
		IMAP_SERVER = imaplib.IMAP4_SSL(MAIL_SERVERS[user2[1]])
		IMAP_SERVER.login(user, password)

	return (IMAP_SERVER)
	
	 
def _configure(fname):
	print("CONFIGURING...")
	f = open(fname, 'w')
	e = raw_input("Enter your email address ")

	while len(e.split("@")) != 2:
		e = raw_input("Enter your email address ")

	f.write(str(e + "\n"))
	f.write(base64.b64encode( getpass.getpass( "Enter your password (stored as base64 encoded str) " )))
	f.close()

def default_date():
	today = datetime.date.today()
	week_ago = today - datetime.timedelta(days=7)
	date_str = str(week_ago.day) + "-" + months[str(week_ago.month)] + "-" + str(week_ago.year)
	return date_str
	
def process_messages(IMAP_SERVER, ids):
	print
	print("=================================")
	ids = [int(x) for x in ids[0].split()]
	ids = list(reversed(ids))
	for id in ids: 
		rv, data = IMAP_SERVER.fetch(int(id), '(RFC822)')
		msg = email.message_from_string(data[0][1])
		print '[%s] From %s; %s' % (id, msg['From'], msg['Subject']) 
	print("=================================")
	print

def get_mailboxes(IMAP_SERVER):
	rv, mailboxes = IMAP_SERVER.list()	
	for mailbox in mailboxes: 
		lst = mailbox.strip('"').split()
		if len(lst) > 3:
			print lst[2].strip('"') + " " + lst[3]
		else:
			print lst[2]

	print()

def get_mails_since_date(IMAP_SERVER, date, flag):
	search_term = '(SINCE "' + date + '" ' + flag + ')' 
	rv, ids = IMAP_SERVER.search(None, search_term)
	return ids

def get_mails_on_date(IMAP_SERVER, date, flag):
	search_term = '(ON "' + date + '" ' + flag + ')' 
	rv, ids = IMAP_SERVER.search(None, search_term)
	return ids

def get_message_by_id(IMAP_SERVER, message_id):	
	rv, data = IMAP_SERVER.fetch(int(message_id), '(BODY.PEEK[TEXT])')
	b = email.message_from_string(data[0][1])
	print '%s: %s' % (message_id, b['Subject']) 
	if b.is_multipart():
		for payload in b.get_payload():
			print payload
	else:
		print dehtml.dehtml(b.get_payload())

def get_messages_by_keyword(IMAP_SERVER, keyword):
	search_term = '(SEARCH "' + keyword + '")'
	rv, ids = IMAP_SERVER.search(None, search_term) 
	return ids	
	

def main():
	global results
	global months  
	global path 

	months = {"1":"Jan", "2":"Feb", "3":"Mar", "4":"Apr", "5":"May", "6":"Jun", "7":"Jul", "8":"Aug", "9":"Sep", "10":"Oct", "11":"Nov", "12":"Dec"}

	parser = argparse.ArgumentParser(description='Simple Terminal Email Client via IMAP')
	ddate = default_date()	

	parser.add_argument("-m", action='store', dest='mailbox', help='Show messages in this mailbox, from the specified date or from the past month (see -d)', default="INBOX")
	parser.add_argument("-d", action='store', dest='date', help='Specify a date in the form of dd-mon-yyyy', default=ddate)
	parser.add_argument("-c", action='store_true', dest='config', help="change the username/password")
	parser.add_argument("-g", action='store', dest="mail_id", help="get a specific message based on its id", type=int)
	parser.add_argument("-s", action='store', dest='keyword', help='search for a message in a mailbox based on a keyword')
	parser.add_argument("-f", action='store', dest='flag', nargs="+", help="search for messages with a certain flag --NOT FULLY SUPPORTED YET (see IMAP search protocol for full list of flags and formats, https://tools.ietf.org/html/rfc3501#section-6.4.4)", default="ALL")
	parser.add_argument("-x", action='store', dest='_delete', help="flag a message as deleted, specified by message id")
	parser.add_argument("--od", action='store', dest="on_date", help="display messages on a specific date, see -d for format", default="")
	parser.add_argument("--sh", action="store_true", dest="act_shell", help="Add flag if you want to open shell", default=False)
	parser.add_argument("--lm", action="store_true", dest="list_mails", help="Add flag if you want to see the mailboxes in your account", default=False)

	results = parser.parse_args()
	IMAP_SERVER = initialize()

	if not results.act_shell:
		if results.config:
			_configure("~/.pistrc")
		if results.list_mails:
			get_mailboxes(IMAP_SERVER)
	
		rv, data = IMAP_SERVER.select(results.mailbox)

		if rv == "NO":
			print("Mailbox", results.mailbox, "not valid")

		elif results.mail_id:
			get_message_by_id(IMAP_SERVER, results.mail_id)	

		elif results.keyword:
			ids = get_messages_by_keyword(IMAP_SERVER, results.keyword)
			process_messages(IMAP_SERVER, ids)

		elif results.on_date: 
			date = results.on_date
			ids = get_mails_on_date(IMAP_SERVER, date, results.flag)
			process_messages(IMAP_SERVER, ids)
		
		elif results._delete:
			pass

		else:
			date = results.date
			ids = get_mails_since_date(IMAP_SERVER, date, results.flag)
			process_messages(IMAP_SERVER, ids)
	
	IMAP_SERVER.logout()

if __name__ == "__main__":
	main()
