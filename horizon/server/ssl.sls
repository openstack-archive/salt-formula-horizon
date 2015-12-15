{%- from "horizon/map.jinja" import server with context %}
{%- if server.ssl.enabled %}

horizon_ssl_packages:
  pkg.installed:
  - names: {{ server.ssl_pkgs }}
  - watch_in:
    - file: horizon_config

{% if grains.os_family == 'RedHat' %}

horizon_apache_ssl_config:
  file.managed:
  - name: /etc/httpd/conf.d/ssl.conf
  - source: salt://horizon/conf/ssl.conf.{{ grains.os_family }}
  - template: jinja
  - mode: 644
  - user: root
  - group: root
  - require:
    - pkg: horizon_packages

{% endif %}

{{ server.certs_dir }}/{{ server.host.name }}.crt:
  file.managed:
  {%- if server.cert is defined %}
  - contents_pillar: horizon:server:cert
  {%- else %}
  - source: salt://pki/{{ server.ssl.authority }}/certs/{{ server.host.name }}.cert.pem
  {%- endif %}
  - require:
    - pkg: horizon_packages
  - require_in:
    - service: horizon_services

{{ server.private_dir }}/{{ server.host.name }}.key:
  file.managed:
  {%- if server.key is defined %}
  - contents_pillar: horizon:server:key
  {%- else %}
  - source: salt://pki/{{ server.ssl.authority }}/certs/{{ server.host.name }}.key.pem
  {%- endif %}
  - require:
    - pkg: horizon_packages
  - require_in:
    - service: horizon_services

{{ server.certs_dir }}/{{ server.ssl.authority }}-chain.crt:
  file.managed:
  {%- if server.chain is defined %}
  - contents_pillar: horizon:server:chain
  {%- else %}
  - source: salt://pki/{{ server.ssl.authority }}/{{ server.ssl.authority }}-chain.cert.pem
  {%- endif %}
  - require:
    - pkg: horizon_packages
  - require_in:
    - service: horizon_services

{%- endif %}