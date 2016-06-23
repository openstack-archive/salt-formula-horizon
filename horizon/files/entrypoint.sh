{%- from "horizon/map.jinja" import server with context -%}
#!/bin/bash -e

cat /srv/salt/pillar/horizon-server.sls | envsubst > /tmp/horizon-server.sls
mv /tmp/horizon-server.sls /srv/salt/pillar/horizon-server.sls

salt-call --local --retcode-passthrough state.highstate

service {{ server.service }} stop || true

export APACHE_RUN_USER=horizon
export APACHE_RUN_GROUP=horizon
export APACHE_PID_FILE=/var/run/apache2/apache2.pid
export APACHE_RUN_DIR=/var/run/apache2
export APACHE_LOCK_DIR=/var/lock/apache2
export APACHE_LOG_DIR=/var/log/apache2

apachectl -DFOREGROUND

{#-
vim: syntax=jinja
-#}
