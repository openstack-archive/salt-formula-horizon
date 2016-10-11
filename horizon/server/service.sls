{%- from "horizon/map.jinja" import server with context %}
{%- if server.enabled %}

horizon_packages:
  pkg.installed:
  - names: {{ server.pkgs }}

horizon_apache_package_absent:
  pkg.purged:
  - name: openstack-dashboard-apache
  - require:
    - pkg: horizon_packages
  - watch_in:
    - service: horizon_services

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

{%- if server.panel is defined %}

{%- for panel_name, panel in server.panel.iteritems() %}

horizon_panel_{{ panel_name }}:
  file.managed:
  - name: /usr/share/openstack-dashboard/openstack_dashboard/local/enabled/_{{ panel.priority }}_{{ panel.dashboard }}_{{ panel_name }}_panel.py
  - source: salt://horizon/files/enabled/panel.py
  - template: jinja
  - mode: 644
  - user: root
  - group: root
  - defaults:
    panel_name: {{ panel_name }}
    panel: {{ panel }}
  - require:
    - pkg: horizon_packages

{%- endfor %}

{%- endif %}

horizon_apache_port_config:
  file.managed:
  - name: {{ server.port_config_file }}
  - source: {{ server.port_config_template }}
  - template: jinja
  - mode: 644
  - user: root
  - group: root
  - require_in:
    - service: horizon_services
  - require:
    - pkg: horizon_packages

horizon_apache_config:
  file.managed:
  - name: {{ server.apache_config }}
  - source: salt://horizon/files/openstack-dashboard.conf.{{ grains.os_family }}
  - template: jinja
  - mode: 644
  - user: root
  - group: root
  - require:
    - pkg: horizon_packages

{%- if grains.os_family == 'Debian' %}
/etc/apache2/conf-enabled/openstack-dashboard.conf:
  file.symlink:
    - target: /etc/apache2/conf-available/openstack-dashboard.conf

apache_enable_wsgi:
  apache_module.enable:
    - name: wsgi
{%- endif %}

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

{%- if grains.get('virtual_subtype', None) == "Docker" %}

horizon_entrypoint:
  file.managed:
  - name: /entrypoint.sh
  - template: jinja
  - source: salt://horizon/files/entrypoint.sh
  - mode: 755

{%- endif %}

{%- endif %}
