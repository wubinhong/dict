#!/usr/bin/env bash

## Logger with timestamp
log() {
    echo "`date -Isecond`    CronTask  ${1}"
}

dump() {
    # Backup mongodb
    mkdir /data/db_back
    dump_dir="/data/db_back/$(date +%Y%m%d_%H%M%S)"
    log ">> Dump mongodb to: ${dump_dir}"
    # mongodump -h 127.0.0.1 -o 20191209_0922
    mongodump -h 127.0.0.1 -o ${dump_dir}
    log "<< Dump finish!"
}

restore() {
    mongorestore -h 127.0.0.1 ${1}
}

case "${1-''}" in
    dump)
        dump
        ;;
    restore)
        log "restore"
        if [ -z "${2}" ]; then
            log "Example: ./cron_backup.sh restore /data/db_back/20191209_092359"
            exit 1
        fi
        restore ${2}
        ;;
    *)
        log "Usage: ./cron_backup.sh <dump | restore 20191209_092359 >"
        ;;
esac
