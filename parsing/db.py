#!/usr/bin/env python
#-*- coding: utf-8 -*-

import MySQLdb
import re

def host_to_db(nag_hostname, nag_hostname_full, nag_parent, info, ip_address, real_address, latitude, longitude):
    new_record = """INSERT INTO new_geo (nag_hostname, nag_hostname_full, nag_parent, info, ip_address, real_address, latitude, longitude)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
    db = MySQLdb.connect(host="localhost", user="***", passwd="***", db="***", charset='utf8')
    add = db.cursor()
    info = re.sub('_', '', info)    
    add.execute(new_record, (nag_hostname.strip(), nag_hostname_full.strip(),nag_parent.strip(), info.strip(),
		ip_address.strip(), real_address.strip(), latitude, longitude))
#    db.close()


def check_in_db(ip_address):
    check_query = """SELECT COUNT(*) FROM new_geo WHERE ip_address='%s'""" % (ip_address)
    db = MySQLdb.connect(host="localhost", user="***", passwd="***", db="***", charset='utf8')
    curs = db.cursor()
    curs.execute(check_query)
    result = curs.fetchone()
    found = result[0]
    return found

def insert_parent_ip(host, parent):
    host = unicode(host, "utf-8")
    check_query = """select ip_address from new_geo where nag_hostname_full='%s'""" % (parent)
    db = MySQLdb.connect(host="localhost", user="***", passwd="***", db="***", charset='utf8', init_command='SET NAMES UTF8')
    curs = db.cursor()
    curs.execute(check_query)
    result = curs.fetchone()
#    print result
    
    if result is not None:
	parent_ip = result[0]
#	print parent_ip
	
#        print host
        curs.close()
        curs = db.cursor()
        insert_query = """UPDATE new_geo SET nag_parent_ip='%s' WHERE nag_hostname_full='%s'""" % (parent_ip, host.strip())
    #    print insert_query
        curs.execute(insert_query )

