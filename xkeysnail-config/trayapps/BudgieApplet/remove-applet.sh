#!/bin/bash

APPLETDIR=/usr/lib/budgie-desktop/plugins

ICONDIR=/usr/share/pixmaps

PROJECT_NAME='org.budgie-desktop.applet.kinto'

echo "Removing Budgie Kinto Applet....."

mkdir -p $APPLETDIR/$PROJECT_NAME

for file in $APPLETDIR/$PROJECT_NAME/*;do
    echo "rm $file"
    # rm $APPLETDIR/$PROJECT_NAME/$file
done

sudo rm -rf $APPLETDIR/$PROJECT_NAME

for file in icons/*; do
	file=${file//icons/}
    echo "rm $ICONDIR$file"
    sudo rm $ICONDIR/$file
done

echo "Finished Removing Kinto Applet. Restart or Re-login to find the applet in Budgie."