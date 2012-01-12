#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# conky-fortune.py - Displays fortune without changing conky's layout
# (C) 2010 Eugenio (g7). All rights reserved.
# Work released under the terms of the GNU GPL license, version 3 or later.
#

import os, commands, sys

size = 27
maxlines = 4

fortune = commands.getoutput("fortune")

if fortune == "No fortunes found":
	sys.exit()

# Split the fortune...
fortune = fortune.split("\n")

output = []
buffer = False

#lol = 0

#len(fortune)

# And now outputting it...
for line in fortune:
	orig = line
	# We should remove the first spaces, if any
	words = line.split("\t")
	for word in words:
		if word == "":
			del words[0]
		else:
			break

	line = " ".join(words)

	# My try to separate the fortunes was not successfully.. eheh - Using fold will resolve this. YAY! :D
	folded = commands.getoutput("echo \"%s\" | fold -w%d" % (line, size))
	folded = folded.split("\n")

	for _line in folded:
		output.append("   " + _line)
	
	# Many fortunes have, as last line, the author. Modify it to put under brackets and in the last citation line.
	#if orig == fortune[-1]:
	#	things = line.split("-")
	#	for thing in things:
	#		if thing == "":
	#			del things[0]
	#	
	#	things = " ".join(things)
	#	auth = "(%s)" % (orig[1:])
	#	print auth
	
	#lol += 1
	#print "loop", lol

	#if buffer:
	#	while buffer != False:
	#		if len(buffer) > size:
	#			#print "BUFF: Outputting %s and buffering %s..." % (buffer[:size], buffer[size:])
	#			output.append(buffer[:size])
	#			buffer = buffer[size:]
	#		else:
	#			#print "BUFF: Outputting %s and disable buffer..." % (buffer)
	#			output.append(buffer)
	#			buffer = False
	#elif len(line) > size:
	#	#print "Outputting %s and activating buffer..." % (line[:size])
	#	output.append(line[:size])
	#	buffer = line[size:]
	#else:
	#	#print "Outputting", line
	#	output.append(line)
	#
	#print "Waiting for next loop..."

if len(output) > maxlines:
	#print "line limit reached, starting another thread..."
	os.system(sys.argv[0])
else:
	#print output
	#print fortune
	for line in output:
		print line
	print ""

#print fortune
