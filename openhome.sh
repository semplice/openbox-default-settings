#!/bin/sh

#
# workaround to open home directory from fbpanel
# (C) 2010 Eugenio "g7" Paolantonio. All rights reserved.
# Released under the terms of the GNU GPL license, version 3 or later.
#

if [ -z "$@" ]; then
	fm="pcmanfm"
else
	fm="$1"
fi

exec $fm "file://$HOME"

# Yes, all here.
