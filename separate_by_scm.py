import subprocess
import time
import sys

# just your average declarations
fin = open('divided', 'r')
hgout = open('hg.todo', 'w')
gitout = open('git.todo', 'w')
divided = fin.readlines()
our_group = 6
process = 0

# loop through the repo list, grabbing each of our repos
for line in divided:
	# grab the group, version control system, and repo name info from the files
	group,scm,name = map(str.strip, line.split(';'))
	group = int(group)
	owner,rname = map(str.strip, name.split('/'))

	# check if the repo is our responsibility
	if group == our_group:
		if scm == 'hg':
			hgout.write('{0}_{1}\n'.format(owner, rname))
		elif scm == 'git':
			gitout.write('{0}_{1}\n'.format(owner, rname))

# clean-up
fin.close()
hgout.close()
gitout.close()
