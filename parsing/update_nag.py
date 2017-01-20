#!/usr/bin/env python
#-*- coding: utf-8 -*-
###############################################################################
#									      #
#                         (C) 2016 Alex Mirtoff				      #
#                        e-mail: alex@mirtoff.ru		              #
#									      #
###############################################################################

import os
import re
import geocode
import db
import sendemail
from datetime import datetime

nagios_dir = '/usr/local/etc/nagios/switches/'
#nagios_dir = '/usr/local/www/nagios/ooonetmap/testconf/'

nagios_all_files = os.listdir(nagios_dir)
only_cfg_files = filter(lambda x: x.endswith('.cfg'), nagios_all_files)
cfg_count = len(only_cfg_files)
loop_count = 0
match_count = 0
match_files_list = []
added = 0
new_hosts = []

def pop_chars(__str__):
	    return re.sub('_', '', __str__)

while loop_count < cfg_count:
	nagios_file = open(nagios_dir+only_cfg_files[loop_count], 'r')
	print only_cfg_files[loop_count]
	nagios_file_str = nagios_file.read()

	hosts_found = re.findall('host_name\s*(-{0,1}[а-яА-Я0-9].*?_\s*)(\s*[^(;|\\n)]*).*?address\s*(\d*.\d*.\d*.\d*).*?parents\s*(.*?[^(\\n|;)]*).*?}', nagios_file_str, re.DOTALL)
	
	for index, item in enumerate(hosts_found):
            if not re.search('alias', item[0]+item[1]) and re.search('[а-яА-Я]', item[0]):
		print("*** Checking HOST in db: %s | %s | %s | %s") % (pop_chars(item[0].strip()), item[1].strip(), item[2].strip(), item[3].strip())
                found = db.check_in_db(pop_chars(item[2]))
                #if re.search('[а-яА-Я]', item[3]):
		#    db.insert_parent_ip(item[0]+item[1], item[3].strip())
		    
		if found == 0:
		    	from_yandex = geocode.yandex_geocode(pop_chars(item[0].strip()))
	     		print("+++ Adding to server: %s \n" % from_yandex[1])
		        db.host_to_db(pop_chars(item[0].strip()), item[0].strip()+item[1].strip(), item[3].strip(), pop_chars(item[1].strip()),
		        item[2].strip(), from_yandex[1], from_yandex[0][0], from_yandex[0][1])
		        new_hosts.append(pop_chars(item[0].strip()))
		        added+=1
        		if re.search('[а-яА-Я]', item[3]):
			    db.insert_parent_ip(item[0]+item[1], item[3].strip())
                else:
                        print('!!! Хост уже существует в БД\n')
									
		match_count+=1
	print 'Найдено всего хостов: ' + str(match_count)
	loop_count+=1
print 'Найдено новых хостов: ' + str(added)

print new_hosts

#script_today = datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S")
#sendemail.script_mail(script_today, str(match_count), str(added), new_hosts, 'Поиск переименованных адресов')


