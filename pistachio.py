#!/usr/bin/env python

"""
ARGS:
	-m selects a mailbox, does default action--shows messages from past week 
	-c configure email & password
	-m -s select a mailbox, search for a keyword in it
	-m -d select a mailbox, show messages from a specific date
	-f specify a flag (UNREAD, ETC.)
	-m -x select a mailbox, delete a specific message (done by id)
	No arg: view messages from past week in inbox 
"""

import argparse 
import imaplib
import email
import getpass

def initialize():

	global PARSER
	global IMAP_SERVER
	global MAIL_SERVERS 

	fname = "pist.conf"
	try: 
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
	print("Configure for ease of use?")
	f.write(input("Enter your email address"))
	f.write(base64.b64encode( getpass.getpass( "Enter your password (stored as base64 encoded str)" )))
	
def process_mailbox(IMAP_SERVER):

def main():
