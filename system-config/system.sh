#!/bin/sh

lowercase(){
	echo "$1" | sed "y/ABCDEFGHIJKLMNOPQRSTUVWXYZ/abcdefghijklmnopqrstuvwxyz/"
}

getOS(){
	OS=$(lowercase `uname`)
	kernel=`uname -r`
	arch=`uname -m`

	OS=`uname`
	if [ "${OS}" = "SunOS" ] ; then
		OS=Solaris
		arch=`uname -p`
		OSSTR="${OS} ${version}(${arch} `uname -v`)"
	elif [ "${OS}" = "AIX" ] ; then
		OSSTR="${OS} `oslevel` (`oslevel -r`)"
	elif [ "${OS}" = "Linux" ] ; then
		if [ -f /etc/redhat-release ] ; then
			distro=`cat /etc/redhat-release |sed s/\ release.*//`
			codename=`cat /etc/redhat-release | sed s/.*\(// | sed s/\)//`
			version=`cat /etc/redhat-release | sed s/.*release\ // | sed s/\ .*//`
			base='RedHat'
		elif [ -f /etc/SuSE-release ] ; then
			codename=`cat /etc/SuSE-release | tr "\n" ' '| sed s/VERSION.*//`
			version=`cat /etc/SuSE-release | tr "\n" ' ' | sed s/.*=\ //`
			base='SuSe'
		elif [ -f /etc/debian_version ] ; then
			if [ -f /etc/lsb-release ] ; then
				distro=`cat /etc/lsb-release | grep '^DISTRIB_ID' | awk -F=  '{ print $2 }'`
				codename=`cat /etc/lsb-release | grep '^DISTRIB_CODENAME' | awk -F=  '{ print $2 }'`
				version=`cat /etc/lsb-release | grep '^DISTRIB_RELEASE' | awk -F=  '{ print $2 }'`
			fi
			base='Debian'
		fi
		if [ -f /etc/UnitedLinux-release ] ; then
			distro="${distro}[`cat /etc/UnitedLinux-release | tr "\n" ' ' | sed s/VERSION.*//`]"
		fi
		OS=`lowercase $OS`
		base=`lowercase $base`
		readonly OS
		readonly distro
		readonly base
		readonly codename
		readonly version
		readonly kernel
		readonly arch
	fi
}
getOS

# echo "OS: $OS"
# echo "base: $base"
# echo "distro: $distro"
# echo "codename: $codename"
# echo "version: $version"
# echo "kernel: $kernel"
# echo "arch: $arch"
# echo ""

# if [ "${distro}" = "Ubuntu" ] ; then
# 	echo "Apply Ubuntu Tweaks"
# fi


