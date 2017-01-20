#!/usr/bin/env python
#-*- coding: utf-8 -*-

import urllib2
import json
import string
import re

def check_location(str):
    region = 'Ставропольский край'
    stv = 'город Ставрополь'
    mih = 'Михайловск '
    nev = 'Невин'

    if re.search(nev, str, re.I):
        url = r'https://geocode-maps.yandex.ru/1.x/?format=json&geocode=%s,+город+%s' % (region, str)
    elif re.search(mih, str, re.I):
        url = r'https://geocode-maps.yandex.ru/1.x/?format=json&geocode=%s,+город+%s' % (region, str)
    else:
       url = r'https://geocode-maps.yandex.ru/1.x/?format=json&geocode=%s,+%s,+%s' % (region, stv, str)
    return url


def yandex_geocode(str):
	str_spl = str.replace('-', ' ')
	str_spl = str.replace('Невинномысск ', 'Невинномысск, ')
	str_spl = str.replace('Михайловск ', 'Михайловск, ')
	url = check_location(str_spl.strip())
	url = url.replace(' ', '+')
#	print "---------------------------"
#	print url
#	print "---------------------------"
	response = urllib2.urlopen(url)
	data = json.loads(response.read())
#	print data
	geo = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split(' ')
#	addr = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['text']
	addr1 = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['description']
	addr2 = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['name']
	addr = addr1+", "+ addr2
        return [[geo[1],geo[0]], addr]




