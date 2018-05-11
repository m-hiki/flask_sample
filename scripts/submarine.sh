#!/bin/sh


NOW=`date +'%Y-%m-%d'`
PROC_ID_FILE_NAME=procId
APP_HOME=/home/opt/submarine
LOGS_DIR=$APP_HOME/logs
SCRIPTS_DIR=$APP_HOME/scripts

echo $SCRIPTS_DIR


start() {
    if [ -f $SCRIPTS_DIR/$PROC_ID_FILE_NAME ]; then
        echo "$SCRIPTS_DIR/$PROC_ID_FILE_NAME file is exist."
        exit 0
    fi

    #nohup python $SCRIPTS_DIR/run-submarine.py > $LOGS_DIR/out.log.$NOW 2>&1 &
    python $SCRIPTS_DIR/run-submarine.py
    PROC_ID=$!
    echo ${PROC_ID} >$SCRIPTS_DIR}/$PROC_ID_FILE_NAME
    echo PID is `cat $SCRIPTS_DIR/$PROC_ID_FILE_NAME`
}


stop() {
    if [ -f $LOCK ]; then
        echo "stop pachira"
        PROC=`cat $LOCK`
        kill $PROC
        rm $LOCK
    fi
    ps -ef |grep pachira |grep -v grep    
}


date +"%Y/%m/%d %H:%M:%S.%N $1"
case "$1" in
  start)
        start "startall"
        ;;
  stop)
        start "startall"
        ;;
esac
date +"%Y/%m/%d %H:%M:%S.%N done."

exit 0