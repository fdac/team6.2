import subprocess
import time

# just your average declarations
fin = open('divided', 'r')
fout = open('pullrequests.todo', 'w')
divided = fin.readlines()
our_group = 6
process = 0

# loop through the repo list, grabbing each of our repos
for line in divided:
	# grab the group, version control system, and repo name info from the files
	group,scm,name = map(str.strip, line.split(';'))
	group = int(group)

	# check if the repo is our responsibility
	if group == our_group:
		fout.write('{0}\n'.format(name))

# clean-up
fin.close()
fout.close()
