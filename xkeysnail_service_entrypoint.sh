#!/bin/bash
#
# This file depicts the entry point for the installation process and decides which
# specialized set of functions to use in the overall process.

# Basic functions to get distro name and version on different distros

# Get distro name from /etc/os-release
function distro_name_from_os_release_file {
	cat /etc/os-release | grep ^NAME= | cut -d'=' -f2
}

# Get distro name from the lsb_release command
function distro_name_from_lsb_release {
	lsb_release -a | grep 'Distributor ID' | cut -d':' -f2 | awk '{$1=$1};1'
}

# Get version from the /etc/os-release file, just to show another variant
function version_from_os_release_file {
	cat /etc/os-release | grep ^VERSION= | cut -d'"' -f2 | cut -d' ' -f1
}

# Get the version on lsb distros like fedora and ubuntu
function version_from_lsb_release {
	lsb_release -a | grep Release | cut -d ':' -f2 | awk '{$1=$1};1'
}

declare -l distro
distro=$(distro_name_from_lsb_release)

# If getting the name via lsb_release does not work, use the /etc/os-release file
#
# This is just an example how I think we can deal with distro differences at the
# start of the intallation procedure.
[ -z $distro ] && distro=$(distro_name_from_os_release_file)
# Add more fallbacks for distros that do not support either of the strategies...

echo "Running on ${distro}"

version=$(version_from_lsb_release) # TODO: also apply some fallback strategy

# This is _all_ conditional logic that deals with distro and version differences,
# so the specific implementations can be neat, understandable and free
# from clutter. Don't fear the code duplication inside the specific scripts. The
# advantages in maintainability greatly outweight the down sides. Also when we
# identify something that clearly is distro and version agnostic that can be
# extracted into a separate script and used everywhere needed.

echo "Using ./linux/installers/$distro$version.sh"
echo "If this leads to a 'No such file or directory' error there is no installer"
echo "for your combination of distro and version. Feel free to contribute one."

source "./linux/installers/$distro$version.sh"

case $1 in
install)
	install
	;;
uninstall)
	uninstall
	;;
*)
	echo "Unsupported mode. Either nothing (intall) or 'uninstall' must be given as the first argument to the script."
	;;
esac
