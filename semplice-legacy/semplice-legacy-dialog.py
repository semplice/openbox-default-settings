#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# semplice-legacy-dialog.py
# Copyright (C) 2015  Semplice Project
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

import quickstart

import os

from gi.repository import Gtk

if os.path.islink(__file__):
	# If we are a link, everything is a WTF...
	DIR = os.path.dirname(os.path.normpath(os.path.join(os.path.dirname(__file__), os.readlink(__file__))))
else:
	DIR = os.path.dirname(__file__)


# While the following is not ideal, is currently needed to make sure
# we are actually on the main semplice-legacy-dialog directory.
# The main executable (this) and all modules do not use absolute paths
# to load the glade UI files, so we need to be on the main directory
# otherwise they will crash.
# This should be probably addressed directly in quickstart.builder but,
# for now, this chdir call will do the job.
os.chdir(DIR)

@quickstart.builder.from_file("./semplice-legacy.glade")
class UI:
	
	events = {
		"destroy" : ["main"],
		"clicked" : ["close_button"],
	}
	
	def exit(self, obj):
		"""
		Exit.
		"""
		
		if self.objects.do_not_display.get_active():
			# Should not display this dialog anymore
			with open(os.path.expanduser("~/.config/.semplice-legacy-dialog-shown"), "w") as f:
				f.write("")
		
		Gtk.main_quit()
	
	on_main_destroy = exit
	on_close_button_clicked = exit
	
	def __init__(self):
		
		self.objects.main.show_all()

quickstart.common.quickstart(UI)
