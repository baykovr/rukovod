#!/usr/bin/env python 
# Texas A&M University
# Department of Computer Science and Engineering
# Robert A. Baykov

import csv
# -- A course contains several sections
class Course(object):
	sections = []
	def __init__(self,name):
		self.name = name
	def add(self,section):
		self.sections.append(section)

# -- Each section has some meta information
# and a list of student objects
# the roster is a csv file, you can get it from csnet.tamu.edu
# A csv line example, simple comma seperated, each line is a student
# 9999999, John, Doe, jdoe, jdoe@tamu.edu, CSCE, U1
class  Section(object):
	# ex : 501 MW 09:10-10:00 RDMC-111H
	students = {}
	def __init__(self,Number,Days,Time,Place,csnet_roster_csv):
		self.Number = Number
		self.Days   = Days
		self.Time   = Time
		self.Place  = Place
		# Parse Roster
		try:
			f = open(csnet_roster_csv, 'rb')
			reader = csv.reader(f)
			rownum = 0
			print 'SECTION ',self.Number
			for row in reader:  
				# Rows which start with # are ignored (comments rows)
				if len(row) > 0 and row[0][0] !='#':
					print row[0] 
					self.students[ row[3] ] = Student(row[0],row[1],row[2],row[3],row[4],row[5],row[6])
				rownum+=1
		except Exception as e:
			print '[ ! ] in Section',e
			exit(1)
		finally:
			f.close()

# -- Student object just holds infromation from the csv file
class Student(object):
	def __init__(self,UIN, LastName, FirstName, Username, Email, Major, Classification):
		self.UIN           = UIN
		self.LastName      = LastName
		self.FirstName     = FirstName
		self.Username      = Username
		self.Email         = Email
		self.Major         = Major
		self.Classification= Classification