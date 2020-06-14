#!/bin/bash

function detect_budgie()
{
	ps -e | grep -E '^.* budgie-wm' > /dev/null
	if [ $? -ne 0 ];
	then
	return 0
	fi
	VERSION=`dpkg-query -l | grep budgie-core | awk '{print $3}'`
	DESKTOP="budgie"
	return 1
}

function detect_gnome()
{
	ps -e | grep -E '^.* gnome-session' > /dev/null
	if [ $? -ne 0 ];
	then
	return 0
	fi
	VERSION=`gnome-session --version | awk '{print $2}'`
	DESKTOP="gnome"
	return 1
}

function detect_kde4()
{
	ps -e | grep -E '^.* kded4$' > /dev/null
	if [ $? -ne 0 ];
	then
		return 0
	else    
		VERSION=`kded4 --version | grep -m 1 'KDE' | awk -F ':' '{print $2}' | awk '{print $1}'`
		DESKTOP="KDE"
		return 1
	fi
}

function detect_kde()
{
	ps -e | grep -E '^.* kded5$' > /dev/null
	if [ $? -ne 0 ];
	then
		return 0
	else    
		VERSION=`kded5 --version | grep -m 1 'KDE' | awk -F ':' '{print $2}' | awk '{print $1}'`
		DESKTOP="KDE"
		return 1
	fi
}

function detect_unity()
{
	ps -e | grep -E 'unity-panel' > /dev/null
	if [ $? -ne 0 ];
	then
	return 0
	fi
	VERSION=`unity --version | awk '{print $2}'`
	DESKTOP="unity"
	return 1
}

function detect_xfce()
{
	ps -e | grep -E '^.* xfce4-session$' > /dev/null
	if [ $? -ne 0 ];
	then
	return 0
	fi
	VERSION=`xfce4-session --version | grep xfce4-session | awk '{print $2}'`
	DESKTOP="xfce"
	return 1
}

function detect_cinnamon()
{
	ps -e | grep -E '^.* cinnamon$' > /dev/null
	if [ $? -ne 0 ];
	then
	return 0
	fi
	VERSION=`cinnamon --version | awk '{print $2}'`
	DESKTOP="cinnamon"
	return 1
}

function detect_mate()
{
	ps -e | grep -E '^.* mate-panel$' > /dev/null
	if [ $? -ne 0 ];
	then
	return 0
	fi
	VERSION=`mate-about --version | awk '{print $4}'`
	DESKTOP="mate"
	return 1
}

function detect_lxde()
{
	ps -e | grep -E '^.* lxsession$' > /dev/null
	if [ $? -ne 0 ];
	then
	return 0
	fi

	# We can detect LXDE version only thru package manager
	which apt-cache > /dev/null 2> /dev/null
	if [ $? -ne 0 ];
	then
	which yum > /dev/null 2> /dev/null
	if [ $? -ne 0 ];
	then
		VERSION='unknown'
	else
		# For Fedora
		VERSION=`yum list lxde-common | grep lxde-common | awk '{print $2}' | awk -F '-' '{print $1}'`
	fi
	else    
	# For Lubuntu and Knoppix
	VERSION=`apt-cache show lxde-common /| grep 'Version:' | awk '{print $2}' | awk -F '-' '{print $1}'`
	fi
	DESKTOP="lxde"
	return 1
}

function detect_sugar()
{
	if [ "$DESKTOP_SESSION" == "sugar" ];
	then
	VERSION=`python -c "from jarabe import config; print config.version"`
	DESKTOP="sugar"
	else
	return 0
	fi
}


DESKTOP="unknown"
if detect_unity;
then
	if detect_kde;
	then
		if detect_kde4;
		then
			if detect_budgie;
			then
				if detect_gnome;
				then
					if detect_xfce;
					then
						if detect_cinnamon;
						then
							if detect_mate;
							then
								if detect_lxde;
								then
									detect_sugar
								fi
							fi
						fi
					fi
				fi
			fi
		fi
	fi
fi


if [ "$1" == '-v' ];
then
	echo $VERSION
else
	if [ "$1" == '-n' ];
	then
	echo $DESKTOP
	else
	echo $DESKTOP $VERSION
	fi
fi