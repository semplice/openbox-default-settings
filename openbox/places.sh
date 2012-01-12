#!/bin/sh

#
# Openbox places pipe menu for Semplice Linux.
# (C) 2010 The Semplice Linux Team. All rights reserved.
# Released under the terms of the GNU GPL v3 license (or later). See /usr/share/common-licenses/GPL.
#

echo '<openbox_pipe_menu>'

echo "<item label=\"$USER\">"
echo "<action name=\"Execute\"><execute>"
echo "pcmanfm file://$HOME"
echo "</execute></action>"
echo "</item>"

echo "<item label=\"Desktop\">"
echo "<action name=\"Execute\"><execute>"
echo "pcmanfm file://$HOME/Desktop"
echo "</execute></action>"
echo "</item>"

echo "<item label=\"Trash\">"
echo "<action name=\"Execute\"><execute>"
echo "pcmanfm trash://"
echo "</execute></action>"
echo "</item>"

echo "<item label=\"Computer\">"
echo "<action name=\"Execute\"><execute>"
echo "pcmanfm computer://"
echo "</execute></action>"
echo "</item>"

echo '<separator />'

# Mounted items

echo "<item label=\"System (/)\">"
echo "<action name=\"Execute\"><execute>"
echo "pcmanfm file:///"
echo "</execute></action>"
echo "</item>"

LANG=C mount | grep "/media" | sed 's/.* on //g' | sed 's/type .*//g' | while read media; do
	echo "<item label=\"`basename \"$media\"`\">"
	echo "<action name=\"Execute\"><execute>"
	echo "pcmanfm \"file://$media\""
	echo "</execute></action>"
	echo "</item>"
done

if [ ! -e "$HOME/.gtk-bookmarks" ]; then
	echo '</openbox_pipe_menu>'
	exit
fi

echo '<separator />'

# Bookmarks (based on: http://david.chalkskeletons.com/scripts/bookmarks.sh)

for bookmark in `cat $HOME/.gtk-bookmarks | awk '{ print $1 }'` ; do
	#echo working in $bookmark
	bookmark=${bookmark#"file://"}
	#bookmark=${bookmark//'%20'/' '}
	echo '<item label="'`basename "${bookmark}"`'">'
	echo '<action name="Execute"><execute>'
	echo "pcmanfm \"file://${bookmark}\""
	echo '</execute></action>'
	echo '</item>'
done

echo '</openbox_pipe_menu>'
