#!/usr/bin/env bash

log()  { echo -e "\x1b[1m[\x1b[93mLOG\x1b[0m\x1b[1m]\x1b[0m ${@}";  }
info() { echo -e "\x1b[1m[\x1b[92mINFO\x1b[0m\x1b[1m]\x1b[0m ${@}"; }
warn() { echo -e "\x1b[1m[\x1b[91mWARN\x1b[0m\x1b[1m]\x1b[0m ${@}"; }

log "Creating directories ..."

mkdir -p /workspace/var/www/html
mkdir -p /workspace/var/cache/lighttpd/uploads
mkdir -p /workspace/var/log/lighttpd/
mkdir -p /workspace/var/run/
mkdir -p /workspace/var/cache/lighttpd/compress/
mkdir -p /workspace/usr/share/lighttpd/
mkdir -p /workspace/etc/lighttpd/conf-enabled/

log "Changing /workspace/ owner to www-data ..."
chown -R www-data: .

cp -r /workspace/etc/* /etc/
>/workspace/var/log/lighttpd/error.log

/usr/local/sbin/lighttpd -f /workspace/lighttpd.conf

log "Trying to connect ..."
curl -s http://127.0.0.1/ I | head -n 1

tail -f /workspace/var/log/lighttpd/error.log
