import re
import pymongo, json

# setup
client = pymongo.MongoClient(host='da0.eecs.utk.edu') # connect to MongoDB
db = client['bitbucket'] # get the bitbucket data
repos = db['repos'] # get the repos
lines = open('divided', 'r').readlines() # the list of repos to handle
our_group = 6 # team 6

# crawl through the repo list, and populate the commits field for each of our repos
for line in lines:
	# parse the line from the divided file
	tokens = map(str.strip, line.strip().split(';'))
	group = int(tokens[0])
	scm = tokens[1]
	name = tokens[2]

	# populate the repo if it's our responsibility
	if group == our_group:
		key = 'https://bitbucket.org/2.0/repositories/' + name
		key = key.strip('\.') # had a repo which ended in a ., which isn't allowed by MongoDB
		url = repos[key]['links']['commits']['href']
