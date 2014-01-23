#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# fix_snapping.py - Snapping fixer
# Copyright (C) 2014  Semplice Project
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# Authors:
#	 Eugenio "g7" Paolantonio <me@medesimo.eu>
#

import xml.etree.ElementTree as etree

import os
import sys

class PIParser(etree.XMLTreeBuilder):
	""" Parser which handles comments, too. 
	
	Taken from http://effbot.org/zone/element-pi.htm
	"""

	def __init__(self):
		 etree.XMLTreeBuilder.__init__(self)
		 # assumes ElementTree 1.2.X
		 self._parser.CommentHandler = self.handle_comment
		 self._parser.ProcessingInstructionHandler = self.handle_pi
		 self._target.start("document", {})

	def close(self):
		 self._target.end("document")
		 return etree.XMLTreeBuilder.close(self)

	def handle_comment(self, data):
		 self._target.start(etree.Comment, {})
		 self._target.data(data)
		 self._target.end(etree.Comment)

	def handle_pi(self, target, data):
		 self._target.start(etree.PI, {})
		 self._target.data(target + " " + data)
		 self._target.end(etree.PI)

def indent(elem, level=0):
	""" Simple indentation for the to-be-written XML.
	
	Taken from http://effbot.org/zone/element-lib.htm#prettyprint
	"""
	
	i = "\n" + level*"  "
	if len(elem):
		if not elem.text or not elem.text.strip():
			elem.text = i + "  "
		if not elem.tail or not elem.tail.strip():
			elem.tail = i
		for elem in elem:
			indent(elem, level+1)
		if not elem.tail or not elem.tail.strip():
			elem.tail = i
	else:
		if level and (not elem.tail or not elem.tail.strip()):
			elem.tail = i

OPENBOX_CONFIGURATION_DIR = os.path.expanduser("~/.config/openbox")

if os.path.exists(os.path.join(OPENBOX_CONFIGURATION_DIR, ".snapupgrade")):
	print("Already upgraded.")
	sys.exit(0)

## Start!

# Open openbox configuration
tree = etree.parse(os.path.join(OPENBOX_CONFIGURATION_DIR, "rc.xml"), PIParser())
document = tree.getroot()
root = document.find("ob:openbox_config", namespaces={"ob":"http://openbox.org/3.5/rc"})
if root is None:
	# openbox-3.4
	root = document.find("ob3:openbox_config", namespaces={"ob3":"http://openbox.org/3.4/rc"})
	namespaces = {"ob":"http://openbox.org/3.4/rc"}
else:
	namespaces = {"ob":"http://openbox.org/3.5/rc"}
etree.register_namespace('',namespaces["ob"])

mouse = root.find("ob:mouse", namespaces=namespaces)

# Search...
for context in mouse.findall("ob:context", namespaces=namespaces):
	if context.get("name") == "Titlebar":
		# This is our context.
		# Now, loop through the bindings to find the one we are looking for.
		for mousebind in context.findall("ob:mousebind", namespaces=namespaces):
			if mousebind.get("button") == "Left" and mousebind.get("action") == "Drag":
				# yay!
				mousebind.clear()
				mousebind.set("button", "Left")
				mousebind.set("action", "Drag")
				
				obj = etree.fromstringlist("""
        <action name="if">
          <!-- Unsnap if snapped-->
          <maximizedvertical>yes</maximizedvertical>
          <then>
            <action name="Unmaximize"/>
              <direction>vertical</direction>
            <action name="MoveResizeTo">
              <x>center</x>
              <!-- we center windows in order to mitigate discrepancies 
              between window placement and mouse cursor -->
              <y>current</y>
            </action>
            <action name="Move"/>
          </then>
          <else>
            <action name="Move"/>
          </else>
        </action>
""", PIParser())
			
				mousebind.append(obj.find("action"))


indent(root)
tree._setroot(root) # fixme?
tree.write(os.path.join(OPENBOX_CONFIGURATION_DIR, "rc.xml"),
	xml_declaration=True,
	encoding="utf-8",
	method="xml"
)


with open(os.path.join(OPENBOX_CONFIGURATION_DIR, ".snapupgrade"), "w") as f:
	f.write("\n")

# Bye!
