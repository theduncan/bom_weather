#!/usr/bin/python2.7
import urllib2  # the lib that handles the url stuff
import MySQLdb
import os
import sys
import re
from string import printable

#DB_Server = os.environ['DB_SERVER']
#DB_User = os.environ['DB_USER']
#DB_Passwd = os.environ['DB_PASSWD']
#DB_DB = os.environ['DB_DB']

DB_Server = 'localhost'
DB_User = 'root'
DB_Passwd = 'theforce'
DB_DB = 'Weather'

db = MySQLdb.connect(DB_Server,DB_User,DB_Passwd,DB_DB )

def DB_create ( db):
    cursor = db.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS `Radar` ( \
      `ID` int(11) DEFAULT NULL, \
      `Product_ID` varchar(8) NOT NULL DEFAULT "********", \
      `STAMP` varchar(12) NOT NULL, \
      `status` varchar(1) NOT NULL DEFAULT "0", \
      `ext` varchar(4) NOT NULL, \
      `url` varchar(255) NOT NULL, \
      `timestamp_downloaded` timestamp NOT NULL DEFAULT "0000-00-00 00:00:00", \
      `timestamp_modified` timestamp NOT NULL DEFAULT "0000-00-00 00:00:00", \
      `timestamp_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP \
      ) ENGINE=innodb DEFAULT CHARSET=latin1; ')

def insert (db, PID, Stamp, ext, url):
    cursor = db.cursor()
    sql_head = """INSERT INTO Radar(`Product_ID`, `STAMP`, `ext`, `url`, `timestamp_modified`) VALUES """
    sql_body = "('%s', '%s', '%s', '%s', now())" % (PID, Stamp, ext, url)
    try:
        # Execute the SQL command
        sql = sql_head + '' + sql_body
        cursor.execute(sql )
        # Commit your changes in the database
        db.commit()
    except MySQLdb.IntegrityError as e:
        if e[0] == 1062:
	    print 'Dup'
	else:
	    print "Error: " + e
            # Rollback in case there is any error
            db.rollback()

cursor = db.cursor()
target_url = 'http://www.bom.gov.au/products/IDR023.loop.shtml'
data = urllib2.urlopen(target_url) # it's a file like object and works just like a file
for line in data: # files are iterable
    if "theImageNames[" in line:
	line2 = line.split(' = ')[1].strip()
	url = re.sub("[^{}]+".format(printable), "", line2.replace(';','').replace('"', ''))
	line3 = url.split('radar/')[1]
	linesplit = line3.split('.')
	PID = linesplit[0]
	STAMP = linesplit[2]
	ext = linesplit[3]
	insert(db, PID, STAMP, ext, url)
	

