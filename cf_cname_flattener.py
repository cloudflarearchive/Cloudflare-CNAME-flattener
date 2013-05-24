#!/usr/bin/env python

import subprocess
import json
import urllib
import socket

#Augh, global variables
CNAME='[INSERT CNAME VALUE HERE]'    # Your CNAME value, i.e. myapp.herokuapp.com
API='[YOUR CLIENT API KEY]'        # Your CloudFlare client API key found at https://www.cloudflare.com/my-account
EMAIL='[YOUR CLOUDFLARE E-MAIL]'   # Your CloudFlare email address
DOMAIN='[CLOUDFLARE DOMAIN NAME]'  # Your CloudFlare domain that you're using this for
RECORD_NAME='[NAME OF RECORD]'     # Use DOMAIN if this is for the root domain


def call_api(params):
	go = urllib.urlopen("https://www.cloudflare.com/api_json.html", params)
	return go.read()

def get_new_ips():
    resolve = socket.gethostbyname_ex(CNAME)
    return resolve[2]

def recordList(): 
	params = urllib.urlencode({
		'a': 'rec_load_all',
		'tkn': API,
		'email': EMAIL,
		'z': DOMAIN})
	return call_api(params)

def getCurrentIPs():
	records = json.loads(recordList())
	ips = dict()
	for record in records['response']['recs']['objs']:
		if record['name'] == RECORD_NAME:
			if record['type'] == 'A':
				ips[record['content']] = record['rec_id']
	return ips

def addRecord(ip):
	params = urllib.urlencode({
		'a': 'rec_new',
		'tkn': API,
		'email': EMAIL,
		'z': DOMAIN,
		'type': 'A',
		'content': ip,
		'ttl': '1',
		'name': RECORD_NAME,
		'service_mode': '1'})
	return call_api(params)

def proxyRecord(rec_id,rtag):
	params = urllib.urlencode({
                'a': 'rec_proxy',
                'tkn': API,
                'email': EMAIL,
                'z': DOMAIN,
                'id': rec_id,
		'rtag': rtag, 
		'service_mode': '1'})
        return call_api(params)

def delRecord(rec_id):
	params = urllib.urlencode({
		'a': 'rec_delete',
		'tkn': API,
		'email': EMAIL,
		'z': DOMAIN,
		'id': rec_id})
	return call_api(params)

def pruneUnused(exclusion, current_records):
	for ip, rec_id in current_records.iteritems():
		if rec_id not in exclusion:
			print "Deleting " + ip
			print delRecord(rec_id)

def compareDNS():
	cf_records = getCurrentIPs()
	cname_ips = get_new_ips()
	do_not_touch = list()	

	for ip in cname_ips:
		if ip not in cf_records:
			print "Adding Record " + ip
			response = json.loads(addRecord(ip))
			proxyRecord(response['response']['rec']['obj']['rec_id'], response['response']['rec']['obj']['rec_tag'])
		else:
			print "Ignoring rec_id: " + cf_records[ip]
			do_not_touch.append(cf_records[ip])
	
	pruneUnused(do_not_touch, cf_records)
		
	
compareDNS()
