{%- from "horizon/map.jinja" import server with context %}
{%- if server.enabled %}

include:
- git
- python

{% if grains.os_family == 'Debian' %}

horizon_packages:
  pkg.installed:
  - names:
    - python-memcache
    - python-psycopg2
    - python-imaging
    - python-docutils
    - python-simplejson
    - build-essential
    - libxslt1-dev
    - libxml2-dev
    - libffi-dev
    - libssl-dev
    - gettext
  - require:
    - pkg: python_packages
  pip.installed:
  - name: lesscpy
  - require:
    - pkg: python_packages

{% endif %}

{% if grains.os_family == 'RedHat' %}

horizon_packages:
  pkg.installed:
  - names:
    - python-imaging
    - python-docutils
    - python-simplejson
    - gettext
  - require:
    - pkg: python_packages
  pip.installed:
  - name: lesscpy
  - require:
    - pkg: python_packages

{%- endif %}

/var/log/horizon:
  file.directory:
  - mode: 770
  - user: horizon
  - group: root

{%- endif %}
