#!/usr/bin/python2.7
import urllib2  # the lib that handles the url stuff
import MySQLdb
import os
import sys
import re
from string import printable
from xml.dom import minidom

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
    cursor.execute('ENGINE=innodb DEFAULT CHARSET=latin1; ')

def insert_region (db, PID, aac, parent_aac, Local_Start, Local_End, UTC_Start, UTC_End, Forecast_Description, Fire_Danger, UV_Alert):
    cursor = db.cursor()
    sql_head = """ INSERT INTO `Forecast_Description`(`Product_ID`, `aac`, `parent-aac`, `Local_Start`, `Local_End`, `UTC_Start`, `UTC_End`, `Forecast_Description`, `Fire_Danger`, `UV_Alert`, `DateTime_Modified`) VALUES   """
    sql_body = "('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s',now())" % (PID, aac, parent_aac, Local_Start, Local_End, UTC_Start, UTC_End, Forecast_Description, Fire_Danger, UV_Alert)
    try:
        # Execute the SQL command
        sql = sql_head + '' + sql_body
        print ('SQL: ', sql)
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
def insert_location (db, PID, aac, parent_aac, Local_Start, Local_End, UTC_Start, UTC_End, icon, min, max, range, precis, pop):
    cursor = db.cursor()
    sql_head = """ INSERT INTO `Forecast_location` (`PID`, `aac`, `parent-aac`, `Local_Start`, `Local_End`, `UTC_Start`, `UTC_End`, `Icon`, `Min`, `Max`, `precipitation_range`, `precis`, `probability_of_precipitation`, `DateTime_Modified`) VALUES   """
    sql_body = "('%s', '%s', '%s', '%s', '%s', '%s', '%s', %d, %d, %d, %s, %s, %s, now())" % (PID, aac, parent_aac, Local_Start, Local_End, UTC_Start, UTC_End, icon, min, max, range, precis, pop)
    try:
        # Execute the SQL command
        sql = sql_head + '' + sql_body
        print ('SQL: ', sql)
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

Fire_Danger = ''
UV_Alert = ''
target_url = 'ftp://ftp2.bom.gov.au/anon/gen/fwo/IDV10450.xml'
data = urllib2.urlopen(target_url) # it's a file like object and works just like a file
xmldoc = minidom.parse(data)
PID = 'IDV10450'
itemlist = xmldoc.getElementsByTagName('area')
print(len(itemlist))
print(itemlist[0].attributes['aac'].value)
for s in itemlist:
    if (s.attributes['aac'].value == 'VIC_ME001'):
	parent_aac = s.attributes['parent-aac'].value
        aac = s.attributes['aac'].value
        forcastlist = s.getElementsByTagName('forecast-period') 
        for f in forcastlist:
            Local_Start =  str(f.attributes['start-time-local'].value)
            Local_End =  str(f.attributes['end-time-local'].value)
            UTC_Start =  str(f.attributes['start-time-utc'].value)
            UTC_End = str(f.attributes['end-time-utc'].value)
            textlist = f.getElementsByTagName('text')
            for t in textlist:
                if (str(t.attributes['type'].firstChild.data) == 'forecast' ):
                    Forecast_Description =  t.firstChild.data
                if (str(t.attributes['type'].firstChild.data) == 'fire_danger' ):
                    Fire_danger =  t.firstChild.data
                if (str(t.attributes['type'].firstChild.data) == 'uv_alert' ):
                    UV_alert =  t.firstChild.data
            insert_region(db, PID, aac, parent_aac, Local_Start, Local_End, UTC_Start, UTC_End, Forecast_Description, Fire_Danger, UV_Alert)
    if (s.attributes['aac'].value == 'VIC_PT042'):
        parent_aac = s.attributes['parent-aac'].value
        aac = s.attributes['aac'].value
        forcastlist = s.getElementsByTagName('forecast-period')
        for f in forcastlist:
            precipitation_range = ''
            icon = '0'
            temp_min = '00'
            temp_max = '00'
            precis = ''
            probability_of_precipitation = ''
            Local_Start =  str(f.attributes['start-time-local'].value)
            Local_End =  str(f.attributes['end-time-local'].value)
            UTC_Start =  str(f.attributes['start-time-utc'].value)
            UTC_End = str(f.attributes['end-time-utc'].value)
            elist = f.getElementsByTagName('element')
            for e in elist:
                if (e.attributes['type'].value == 'forecast_icon_code'):
                    icon = e.firstChild.data
                    print 'ICON: ' + icon
                if (e.attributes['type'].value == 'precipitation_range'):
                    precipitation_range = e.firstChild.data
                    print 'precipitation_range: ' + precipitation_range
                if (e.attributes['type'].value == 'air_temperature_minimum'):
                    temp_min = e.firstChild.data
                    print 'temp_min: ' + temp_min
                if (e.attributes['type'].value == 'air_temperature_maximum'):
                    temp_max = e.firstChild.data
                    print 'temp_max: ' + temp_max
                if (e.attributes['type'].value == 'precis'):
                    precis = e.firstChild.data
                    print 'precis: ' + precis                
                if (e.attributes['type'].value == 'probability_of_precipitation'):
                    probability_of_precipitation = e.firstChild.data
                    print 'probability_of_precipitation: ' + probability_of_precipitation  
            if (temp_min != '00'):
                insert_location (db, PID, aac, parent_aac, Local_Start, Local_End, UTC_Start, UTC_End, int(icon), int(temp_min), int(temp_max), precipitation_range, precis, probability_of_precipitation)