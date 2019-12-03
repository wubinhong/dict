#!/usr/bin/env bash

## Logger with timestamp
log() {
    echo "`date -Isecond`    ${1}"
}

# Backup mongodb
backup_file="/data/configdb/Word_$(date +%Y%m%d_%H:%M:%S).json"
log ">> Backup mongodb to: ${backup_file}"
mongoexport --uri=mongodb://127.0.0.1:27017/dict -c Word -o ${backup_file}
log "<< Backup finish!"
