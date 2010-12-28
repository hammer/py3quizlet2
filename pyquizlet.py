import ConfigParser
import httplib
import json
import os
import urllib

# TODO(hammer): use mxURL, urlparse, or urllib to make working with URLs cleaner

api_base_url = '/api/1.0/sets'

config = ConfigParser.ConfigParser()
config.readfp(open(os.path.expanduser('~/.pyquizlet')))

request_parameters = [('dev_key', config.get('QUIZLET', 'dev_key')),
                      ('q', 'creator:%s' % config.get('QUIZLET', 'username')),
                      ('sort', 'most_recent'),
                      ('extended', 'on'),
                      ('whitespace', 'off'),
                     ]

quizlet_connection = httplib.HTTPConnection('quizlet.com')
request_string = api_base_url + '?' + urllib.urlencode(request_parameters)
quizlet_connection.request('GET', request_string)
response = quizlet_connection.getresponse()

if response.status != 200:
  print "Failed request with status %s." % response.status

try:
  response_data = json.load(response)
except Exception, e:
  print 'Problem parsing response: %s' % e

if response_data['response_type'] == 'error':
  print "Failed request: %s: %s" % (response_data['short_text'], response_data['long_text'])

print response_data['sets']

quizlet_connection.close()
