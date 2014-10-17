#!/usr/bin/env python 
# Texas A&M University
# Department of Computer Science and Engineering
# Robert A. Baykov

import sys,datetime,time,csv,os,argparse,smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText      import MIMEText
from rukovod_datatypes   import Course,Section,Student


# TODO: gpg signing
USE_CRYPTO = False 

# number of seconds to wait in between sending emails
TIME_DELAY = 1 

# email from field, ie something@something.edu
EMAIL_FROM = 'REDACTED'

# email authentications, ie password for something@something.edu
EMAIL_AUTH = 'REDACTED'

# email subject
EMAIL_SUBJ = 'REDACTED'

# default, our load balanced smtp relay
SMTP_RELAY      = "smtp-relay.tamu.edu"
SMTP_RELAY_PORT = 25


# -- from toolbox.py http://github.com/baykovr/toolbox
# -- Some common functions 
def f_as_list(filename):
	# Note: will strip out new line characters
	# Return file contents as a list
	# each line is a new item 
	try:
		line_list = []
		fp = open(filename)
		for line in fp:
			line = line.strip('\r\n')
			line_list.append(line)
		return line_list
	except Exception, e:
		print '[ ! ] in f_getlist',e
		return -1
def pipe_cmd(command):
	try:
		return os.popen(command).read()
	except Exception as e:
		print e
		return -1
def cmd(cmd):
	print 'Trying to exec:',cmd
	try:
		suppression = "&>/dev/null"
		return os.system(cmd)
	except Exception as e:
		print   e
		return -1	

def send_mail(fromaddr,toaddr,subject,body,username,password):
	msg = MIMEMultipart()
	msg['From']    = fromaddr
	msg['To']      = toaddr
	msg['Subject'] = subject
	msg.attach(MIMEText(body, 'plain'))
	server = smtplib.SMTP(SMTP_RELAY, SMTP_RELAY_PORT)
	server.ehlo()
	server.starttls()
	server.ehlo()
	# smtp credentials
	server.login(username, password)
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)

# -- This parses the course file
# the course file holds some course meta information
# Line 1 is the course name
# subsequent lines after that are sections (multiple)
# COURSE CSCE-999
# SECTION 500-600 TR 08:00-09:10 HRBB-999 rosters/roster.csv
def init_course_file(course_file):
	COURSE = None
	info = f_as_list(course_file)

	for line in info:
		line = line.split(' ')
		if line[0]  == 'COURSE':
			COURSE = Course(line[1])
		elif line[0] == 'SECTION':
			COURSE.add(Section(line[1],line[2],line[3],line[4],line[5]))

	print 'Loaded '
	print 'Course  : ',COURSE.name
	print 'Sections: ',

	# Now you can do some actions, such as dump all emails
	# for section in COURSE.sections:
	# 	print '=== SECTION:',section.Number
	# 	for username in section.students:
	# 		#print username, 
	# 		print section.students[username].Email,','
	return COURSE

# -- MAIL / CRYPTO --
def mail_unsigned_feedback(dst_addr,feedback):
	print 'mailing'
	print 'UNCOMMENT rukovod.py@110 to actually send.'
	#send_mail(EMAIL_FROM,dst_addr,EMAIL_SUBJ,feedback,EMAIL_FROM,EMAIL_AUTH)

def mail_signed_feedback(dst_addr,feedback):
	print 'mailing-signed'
	#TODO GPG



# The generic gradebook file has arbitrary columns
# Markup 
def process_generic_grades_file(grades_file):
	
	email_list = []

	print '[...] FILE   :',grades_file
	print '[ ! ] WARNING: always double check email / roster records against this csv before mailing.'
	ok = raw_input('[ ? ] continue (y/N):')
	if ok.lower() != 'y':
		print 'Exiting.'
		return
	try:
		f = open(grades_file, 'rb')
		reader = csv.reader(f)
		header = ''
		total_rows = 0

		for row in reader:
			if total_rows == 0:
				header = row
				# -- Header --
				header_row_index   = 0
				for header_row in header:
					if 'email' in header_row.lower():
						email_dst_index = header_row_index
						break
					header_row_index+=1
					
				# If no such column found offer debug and exit
				if email_dst_index == -1:
					print '\n[ ! ] could not locate an email address column'
					nok = raw_input('[ ? ] show checked columns (y/N):')
					if nok.lower() == 'y':
						header_row_index=0
						for header_row in header:
							print '\t[',header_row_index,']',header_row
							header_row_index+=1
					print 'Check columns, Exiting.'
					return
				# -- /Header --
			# -- Data Rows --
			else:
				
				# Construct Email Body
				# Column : Data
				# Column : Date 
				# etc ... 
				email_body = ''
				email_dest = row[email_dst_index]

				email_body += 'BEGIN-MESSAGE'+'*'*40 +'\n'
				for i in range(0,len(header)):	
					email_body += header[i].ljust(12) + ' ' + row[i] + '\n'
				email_body += 'END-MESSAGE'+'*'*42+'\n'

				email_list.append( (email_dest,email_body) )
			# -- /Data Rows --
			total_rows+=1

		# Check
		if total_rows-1 == 0:
			print '[ ! ] 0 rows found, nothing to do.'

		print '[...] total entries extracted:',total_rows-1 # minus header
		print '[...] estimated time to send :',TIME_DELAY*total_rows-1,'(seconds)'
		
		if len(email_list) > 0:
			ok = raw_input('[ ? ] preview first message (y/N)')
			if ok.lower() == 'y':
				print 'DESTINATION:',email_list[0][0]
				print email_list[0][1]
				
			ok = raw_input('\n[ ! ] SEND ALL MAIL (y/N)')
			if ok.lower() == 'y':
				# MAIL-AWAY
				for email in email_list:
					# Dump to stdout for record
					print 'MAILING',datetime.datetime.now()
					print 'DESTINATION:',email[0]
					print email[1]

					# Mail
					if USE_CRYPTO == True:
						mail_signed_feedback(email[0],email[1])
					else:
						mail_unsigned_feedback(email[0],email[1])
					# Wait
					time.sleep(TIME_DELAY)
			else:
				print 'Exiting.'
				return
		else:
			print '[ ! ] no mail to send, exiting.'

	except Exception as e:
		print '[ ! ]',e
		exit(1)
	finally:
		f.close()


if __name__ == "__main__":
	try:
		# TODO, PGP
		pass
	except Exception as e:
		print '[ ! ]',e
		ok = raw_input('[ ? ] continue without crypto (y/N):')
		if ok.lower() == 'y':
			USE_CRYPTO = False
		else:
			print 'Exiting.'
			exit(0)

	# Parse Args
	parser = argparse.ArgumentParser(description='rukovod')
	group = parser.add_mutually_exclusive_group()
	group.add_argument('-c','--course',help='Course file',type=str)
	group.add_argument('-g','--grades',help='Grades file',type=str)

	arguments = parser.parse_args()

	if arguments.course:
		COURSE = init_course_file(arguments.course)
		
	elif arguments.grades:
		process_generic_grades_file(arguments.grades)
	else:
		print '-c / --course COURSE_FILE'
		print '-g / --grades GRADES_FILE'