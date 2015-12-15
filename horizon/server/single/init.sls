{%- from "horizon/map.jinja" import server with context %}
{%- if server.enabled %}

{%- if server.ssl is defined %}
include:
- horizon.server.single.ssl
{%- endif %}

{%- if grains.os == "ubuntu" %}

horizon_ubuntu_theme_absent:
  pkg.purged:
  - name: openstack-dashboard-ubuntu-theme

{%- endif %}

{%- for plugin_name, plugin in server.get('plugin', {}) %}

horizon_{{ plugin_name }}_package:
  pkg.installed:
  - name: {{ plugin.source.name }}
  - watch_in:
    - service: horizon_services

{%- endfor %}

horizon_packages:
  pkg.installed:
  - names: {{ server.pkgs }}

horizon_config:
  file.managed:
  - name: {{ server.config }}
  - source: salt://horizon/files/local_settings/{{ server.version }}_settings.py
  - template: jinja
  - mode: 644
  - user: root
  - group: root
  - require:
    - pkg: horizon_packages

{%- if grains.os_family == 'RedHat' %}

horizon_apache_port_config:
  file.managed:
  - name: /etc/httpd/conf/httpd.conf
  - source: salt://horizon/conf/httpd.conf.RedHat
  - template: jinja
  - mode: 644
  - user: root
  - group: root
  - require_in:
    - service: horizon_services
  - require:
    - pkg: horizon_packages

{%- endif %}

{%- if grains.os_family == 'Debian' %}

horizon_apache_port_config:
  file.managed:
  - name: /etc/apache2/ports.conf
  - source: salt://horizon/conf/ports.conf
  - template: jinja
  - mode: 644
  - user: root
  - group: root
  - require_in:
    - service: horizon_services
  - require:
    - pkg: horizon_packages

{%- endif %}

horizon_apache_config:
  file.managed:
  - name: {{ server.apache_config }}
  - source: salt://horizon/conf/openstack-dashboard.conf.{{ grains.os_family }}
  - template: jinja
  - mode: 644
  - user: root
  - group: root
  - require:
    - pkg: horizon_packages

horizon_services:
  service.running:
  - name: {{ server.service }}
  - enable: true
  - watch:
    - file: horizon_config
    - file: horizon_apache_config
    - file: horizon_log_file

horizon_log_dir:
  file.directory:
    - name: /var/log/horizon
    - user: horizon
    - group: adm
    - mode: 750

horizon_log_file:
  file.managed:
    - name: /var/log/horizon/horizon.log
    - user: horizon
    - group: adm
    - mode: 640
    - require:
      - file: horizon_log_dir

{#
{%- if server.get('api_versions', {}).identity is defined %}

horizon_keystone_policy:
  file.managed:
  - name: /usr/share/openstack-dashboard/openstack_dashboard/conf/keystone_policy.json
  {%- if server.get('api_versions', {}).identity == '3' %}
  - source: salt://horizon/files/policy/{{ server.version }}-keystone-v3.json
  {%- else %}
  - source: salt://horizon/files/policy/{{ server.version }}-keystone-v2.json
  {%- endif %}

{%- endif %}

{%- if server.logging is defined %}

# TODO: package this
raven:
  pip.installed:
    - name: raven >= 4

{%- endif %}
#}

{%- endif %}
