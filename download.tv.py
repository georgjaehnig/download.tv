#!/usr/bin/python

import urllib
import json
import sys
from urlparse import urlparse

if len(sys.argv) != 2:
	sys.exit(1)

slug =  urlparse(sys.argv[1]).fragment.split('/')[2] # "slug" - z.B. 'vor-20-jahren-autounfall'


apihost = 'http://spiegeltv-ivms2-restapi.s3.amazonaws.com';

vn = json.loads(urllib.urlopen('%s/version.json' % apihost).read())['version_name']
oid = json.loads(urllib.urlopen('%s/%s/restapi/slugs/%s.json' % (apihost, vn, slug)).read())['object_id']
uuid = json.loads(urllib.urlopen('%s/%s/restapi/media/%s.json' % (apihost, vn, oid)).read())['uuid']
is_wide = json.loads(urllib.urlopen('%s/%s/restapi/media/%s.json' % (apihost, vn, oid)).read())['is_wide']
server = json.loads(urllib.urlopen('http://www.spiegel.tv/streaming_servers/').read())[0]['endpoint']

if is_wide:
	format = '16x9'
else:
	format = '4x3'

print("rtmpdump -r %smp4:%s_spiegeltv_0500_%s.m4v -o %s.mp4" % (server, uuid, format, slug))

