#!/bin/bash
#
# chkconfig: 35 90 12
# description: Kinto service
#

# Get function from functions library
# . /etc/init.d/functions

# Start the service
start() {
        echo -n "Starting Kinto (xkeynsail)" | logger
        xkeycount=$(pgrep 'xkeysnail' | wc -l)

        if [[ $xkeycount -eq 0 ]]; then
            /usr/bin/xhost +SI:localuser:root && script -q -c "xkeysnail --quiet --watch `echo $HOME`/.config/kinto/kinto.py" /dev/null | tee -a /tmp/kinto.log &
            ### Create the lock file ###
            touch /var/lock/subsys/kinto
            success $"Kinto (xkeynsail) started"
        else
            echo "Kinto (xkeynsail) service is already running."
        fi
        
        echo
}

# Restart the service
stop() {
        echo -n "Stopping Kinto (xkeynsail)" | logger
        sudo pkill -f bin/xkeysnail >/dev/null 2>&1
        ### Now, delete the lock file ###
        rm -f /var/lock/subsys/kinto
        echo
}

### main logic ###
case "$1" in
  start)
        start
        ;;
  stop)
        stop
        ;;
  status)
        status
        ;;
  restart|reload|condrestart)
        stop
        sleep 5
        start
        ;;
  *)
        echo $"Usage: $0 {start|stop|restart|reload|status}"
        exit 1
esac

exit 0