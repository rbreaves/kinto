#!/bin/bash
#Budgie Kinto Applet
#This script basically just copies the files to approproate directories.

APPLETDIR=/usr/lib/budgie-desktop/plugins

ICONDIR=/usr/share/pixmaps

PROJECT_NAME='org.budgie-desktop.applet.kinto'

echo "Installing Budgie Kinto Applet....."

mkdir -p $APPLETDIR/$PROJECT_NAME

for file in KintoApplet/*;do
    install -m 0755 "$file" $APPLETDIR/$PROJECT_NAME/
done

for file in icons/*; do
    install -m 0755 "$file" $ICONDIR/
done

echo "Finished Installing Applet. Restart or Re-login to find the applet in Budgie."
