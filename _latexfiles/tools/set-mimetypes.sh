#!/bin/bash

IFS=$'\n'

SVNURL=https://repos.ivt.ethz.ch/svn/ivt/doc/trunk
SVNTMP=tmp

rm -rf $SVNTMP
svn checkout $SVNURL $SVNTMP
pushd $SVNTMP
for FILE in $(find * -name .svn -prune -or -type f); do
	SVNFILE=${FILE}
	SVNPROP=$(svn propget svn:mime-type ${SVNFILE})
	MIMETYPE=$(mimetype -b $FILE)
	echo $SVNFILE
	if [ "$SVNPROP" != "$MIMETYPE" ]; then
		echo $SVNPROP "->" $MIMETYPE
		svn propset svn:mime-type "$MIMETYPE" $SVNFILE
	else
		echo $SVNPROP
	fi
done
popd


