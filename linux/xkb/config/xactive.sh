#!/bin/bash

if [ $# -eq 0 ]
  then
    # No arguments
    ./kintox11
else
	./caret_status.sh &
	./kintox11
fi
