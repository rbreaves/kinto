#!/usr/bin/env bash

# /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/rbreaves/kinto/master/install/linux.sh)"

# Find a download directory dynamically to support non-default XDG user dir.
# In case the `xdg-user-dir` is not installed, fallback to the hardcoded path
DOWNLOADS_DIR=$(xdg-user-dir DOWNLOAD || echo "${HOME}/Downloads")

wget https://github.com/rbreaves/kinto/archive/refs/heads/master.zip -O ${DOWNLOADS_DIR}/kinto.zip || curl https://github.com/rbreaves/kinto/archive/refs/heads/master.zip -J -L -o ${DOWNLOADS_DIR}/kinto.zip
unzip ${DOWNLOADS_DIR}/kinto.zip -d ${DOWNLOADS_DIR}/
cd ${DOWNLOADS_DIR}/kinto-master/

kintorelease=`wget -qO- https://api.github.com/repos/rbreaves/kinto/releases/latest | awk -F'tag_name": ' '{if ($2) print $2}' | tr -d \", || curl -s https://api.github.com/repos/rbreaves/kinto/releases/latest | awk -F'tag_name": ' '{if ($2) print $2}' | tr -d \",`
kintohash=`unzip -z ${DOWNLOADS_DIR}/kinto.zip | tail -n1`
kintoshort=${kintohash::7}

echo "$kintorelease" "build" "$kintoshort" > ./dl_version

if [ $# -eq 0 ];then
	echo "Installing Kinto..."
	./setup.py
elif [ $1 == "-r" ];then
	echo "Uninstall Kinto..."
	./setup.py -r
fi
