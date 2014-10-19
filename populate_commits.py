import re
import pymongo, json

client = pymongo.MongoClient(host='da0.eecs.utk.edu')
db = client['bitbucket']
lines = open('divided', 'r').readlines()
our_group = 6

repos = db['repos']
for line in lines:
	tokens = map(str.strip, line.strip().split(';'))
	group = int(tokens[0])
	scm = tokens[1]
	name = tokens[2]

	if group == our_group:
		key = 'https://bitbucket.org/2.0/repositories/' + name
		key = key.strip('\.')
		url = repos[key]['links']['commits']['href']
