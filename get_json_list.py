import subprocess
import time
import sys

# just your average declarations
which = sys.argv[1]
fin = open('divided', 'r')
fout = open(which + '.todo', 'w')
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
