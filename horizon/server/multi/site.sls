{%- from "horizon/map.jinja" import server with context %}
{%- if server.enabled %}

include:
- git

horizon_user:
  user.present:
  - name: horizon
  - system: True
  - home: /srv/horizon

/var/log/horizon:
  file.directory:
  - mode: 770
  - user: horizon
  - group: root
  - require:
    - user: horizon_user

/srv/horizon/sites:
  file.directory:
  - makedirs: true

{%- for app_name, app in server.app.iteritems() %}

{%- if app.get('dashboard', 'openstack') in ['openstack', 'helpdesk'] %}
{%- if app.get('version', 'juno') in ['juno', 'kilo', 'liberty', 'mitaka'] %}
{%- set config_file = "/srv/horizon/sites/"+app_name+"/lib/python" + pillar.python.environment.get("version", "2.7") + "/site-packages/openstack_dashboard/local/local_settings.py" %}
{%- else %}
{%- set config_file = "/srv/horizon/sites/"+app_name+"/extra/openstack_dashboard/local/local_settings.py" %}
{%- endif %}
{%- elif app.get('dashboard', 'openstack') == 'csb' %}
{%- set config_file = "/srv/horizon/sites/"+app_name+"/plugins/csb_dashboard/csb_dashboard/local/local_settings.py" %}
{%- elif app.get('dashboard', 'openstack') == 'robotice' %}
{%- set config_file = "/srv/horizon/sites/"+app_name+"/plugins/robotice_dashboard/robotice_dashboard/local/local_settings.py" %}
{%- endif %}

{%- if app.plugin.contrail is defined %}
{%- set requirements = "contrail" %}
{%- else %}
{%- set requirements = "vanilla" %}
{%- endif %}

/srv/horizon/sites/{{ app_name }}:
  virtualenv.manage:
  - system_site_packages: False
  - requirements: salt://horizon/files/requirements/{{ app.version }}_{{ requirements }}.txt
  - require:
    - file: /srv/horizon/sites
    - pkg: horizon_packages

{{ app_name }}_{{ app.source.address }}:
  git.latest:
  - name: {{ app.source.address }}
  - target: /srv/horizon/sites/{{ app_name }}/extra
  {%- if grains.saltversioninfo.0 > 2015 %}
  - rev: HEAD
  - branch: {{ app.source.revision }}
  {%- else %}
  - rev: {{ app.source.revision }}
  {%- endif %}
  - submodules: True
  - require:
    - virtualenv: /srv/horizon/sites/{{ app_name }}
    - pkg: git_packages

horizon_{{ app_name }}_dirs:
  file.directory:
  - names:
    - /srv/horizon/sites/{{ app_name }}/media
    - /var/log/horizon
  - mode: 777
  - user: horizon
  - group: horizon
  - require:
    - git: {{ app_name }}_{{ app.source.address }}

horizon_{{ app_name }}_logs:
  file.managed:
  - names:
    - /var/log/horizon/{{ app_name }}_app.log
    - /var/log/horizon/{{ app_name }}_error.log
    - /var/log/horizon/{{ app_name }}_gunicorn.log
    - /var/log/horizon/{{ app_name }}_horizon.log
  - user: horizon
  - group: horizon
  - replace: False
  - require:
    - file: horizon_{{ app_name }}_dirs

{%- if app.get('version', 'juno') in ['juno', 'kilo', 'helpdesk', 'liberty', 'mitaka'] %}

horizon_setup_{{ app_name }}_horizon:
  cmd.run:
  - names:
    - source /srv/horizon/sites/{{ app_name }}/bin/activate; python setup.py install
  - cwd: /srv/horizon/sites/{{ app_name }}/extra
  - require:
    - git: {{ app_name }}_{{ app.source.address }}
  - require_in:
    - file: horizon_{{ app_name }}_config

{%- if app.get('api_versions', {}).identity is defined %}
{%- if app.get('api_versions', {}).identity == '3' %}

horizon_{{ app_name }}_config:
  file.managed:
  - name: /srv/horizon/sites/{{ app_name }}/lib/python{{ pillar.python.environment.get("version", "2.7") }}/site-packages/openstack_dashboard/conf/keystone_policy.json
  - source: salt://horizon/files/policy/{{ app.version }}-keystone-v3.json
  - require:
    - cmd: horizon_setup_{{ app_name }}_horizon

{%- endif %}
{%- endif %}

{%- endif %}

{%- if app.get('version', 'juno') in ['kilo', 'helpdesk', 'liberty', 'mitaka'] %}

/srv/horizon/sites/{{ app_name }}/static:
  file.symlink:
  - target: /srv/horizon/sites/{{ app_name }}/local/lib/python2.7/site-packages/static
  - mode: 777
  - user: root
  - group: root
  - require:
    - git: {{ app_name }}_{{ app.source.address }}

horizon_{{ app_name }}_config:
  file.managed:
  - name: /srv/horizon/sites/{{ app_name }}/lib/python{{ pillar.python.environment.get("version", "2.7") }}/site-packages/openstack_dashboard/local/local_settings.py
  - source: salt://horizon/files/local_settings/{{ app.version }}_settings.py
  - template: jinja
  - mode: 644
  - user: root
  - group: root
  - defaults:
    app_name: {{ app_name }}
  - require_in:
    - file: /srv/horizon/sites/{{ app_name }}/manage.py

{%- else %}

/srv/horizon/sites/{{ app_name }}/static:
  file.directory:
  - mode: 777
  - user: root
  - group: root
  - require:
    - git: {{ app_name }}_{{ app.source.address }}

horizon_{{ app_name }}_config:
  file.managed:
  - name: {{ config_file }}
  - source: salt://horizon/files/local_settings/{{ app.version }}_settings.py
  - template: jinja
  - mode: 644
  - user: root
  - group: root
  - defaults:
    app_name: {{ app_name }}
  - require_in:
    - file: /srv/horizon/sites/{{ app_name }}/manage.py

{%- endif %}

/srv/horizon/sites/{{ app_name }}/manage.py:
  file.managed:
  - source: salt://horizon/files/manage.py
  - template: jinja
  - mode: 777
  - user: root
  - group: root
  - defaults:
    app_name: {{ app_name }}

/srv/horizon/sites/{{ app_name }}/wsgi.py:
  file.managed:
  - source: salt://horizon/files/wsgi.py
  - template: jinja
  - mode: 644
  - user: root
  - group: root
  - defaults:
    app_name: {{ app_name }}
  - require:
    - git: {{ app_name }}_{{ app.source.address }}

{%- if app.plugin.merlin_panels is defined %}

/srv/horizon/sites/{{ app_name }}/database.db:
  file.managed:
  - mode: 666
  - user: horizon
  - group: horizon
  - require:
    - git: {{ app_name }}_{{ app.source.address }}

{%- endif %}

{#
{%- for dashboard_name, dashboard in app.plugin.iteritems() %}
{%- endfor %}
#}

{%- if app.plugin is defined %}

/srv/horizon/sites/{{ app_name }}/plugins:
  file.directory:
  - makedirs: True
  - require:
    - git: {{ app_name }}_{{ app.source.address }}

{%- for dashboard_name, dashboard in app.get('dashboards', {}).iteritems() %}

{%- if app.get('version', 'juno') in ['kilo', 'helpdesk', 'liberty', 'mitaka'] %}

horizon_{{ app_name }}_{{ dashboard_name }}_config:
  file.managed:
  - name: /srv/horizon/sites/{{ app_name }}/lib/python{{ pillar.python.environment.get("version", "2.7") }}/site-packages/openstack_dashboard/enabled/_{{ dashboard.get('order', 70) }}_{{ dashboard_name }}.py
  - source: salt://horizon/files/enabled/{{ dashboard_name }}.py
  - template: jinja
  - mode: 644
  - user: root
  - group: root
  - defaults:
    app_name: {{ app_name }}
    enabled: {{ dashboard.enabled }}
  - require:
    - git: {{ app_name }}_{{ app.source.address }}

{%- endif %}

{%- endfor %}


{%- for plugin_name, plugin in app.plugin.iteritems() %}

{%- if app.get('version', 'juno') in ['kilo', 'helpdesk', 'liberty', 'mitaka'] %}

horizon_{{ app_name }}_{{ plugin_name }}_config:
  file.managed:
  - name: /srv/horizon/sites/{{ app_name }}/lib/python{{ pillar.python.environment.get("version", "2.7") }}/site-packages/openstack_dashboard/local/enabled/_{{ plugin.get('
  ', 60) }}_{{ plugin_name }}.py
  - source: salt://horizon/files/enabled/{{ plugin_name }}.py
  - template: jinja
  - mode: 644
  - user: root
  - group: root
  - defaults:
    app_name: {{ app_name }}
  - require:
    - git: {{ app_name }}_{{ app.source.address }}

{%- endif %}

{{ app_name }}_{{ plugin_name }}:
  {{ plugin.source.engine }}.latest:
  - name: {{ plugin.source.address }}
  - target: /srv/horizon/sites/{{ app_name }}/plugins/{{ plugin_name }}
  {%- if grains.saltversioninfo.0 > 2015 %}
  - rev: HEAD
  - branch: {{ plugin.source.revision }}
  {%- else %}
  - rev: {{ plugin.source.revision }}
  {%- endif %}
  - submodules: True
  - require:
    - file: /srv/horizon/sites/{{ app_name }}/plugins
  - require_in:
    - cmd: horizon_setup_{{ app_name }}

{%- if plugin_name == "contrail" and app.get("version", "juno") in ["juno", "kilo", 'helpdesk', 'liberty', 'mitaka'] %}

fix_contrail_{{ app_name }}:
  cmd.run:
  - name: source /srv/horizon/sites/{{ app_name }}/bin/activate; pip install git+https://github.com/Juniper/python-neutronclient.git@contrail/juno#egg=python-neutronclient --upgrade --no-deps
  - cwd: /srv/horizon/sites/{{ app_name }}

{%- endif %}

{%- if plugin_name == "horizon_theme" and app.get("version", "juno") in ["kilo", 'helpdesk'] %}

/srv/horizon/sites/{{ app_name }}/local/lib/python2.7/site-packages/openstack_dashboard/dashboards/theme:
  file.symlink:
  - target: /srv/horizon/sites/{{ app_name }}/plugins/{{ plugin_name }}/horizon_theme/dashboards/theme
  - user: root
  - group: root
  - require:
    - git: {{ app_name }}_{{ app.source.address }}

/srv/horizon/sites/{{ app_name }}/local/lib/python2.7/site-packages/openstack_dashboard/static/themes/{{ plugin.theme_name }}:
  file.symlink:
  - target: /srv/horizon/sites/{{ app_name }}/plugins/{{ plugin_name }}/horizon_theme/dashboards/theme/static/themes/{{ plugin.theme_name }}
  - user: root
  - group: root
  - require:
    - git: {{ app_name }}_{{ app.source.address }}

{%- elif plugin_name == "horizon_theme" and app.get("version", "liberty") in ['liberty', 'mitaka'] %}

/srv/horizon/sites/{{ app_name }}/local/lib/python2.7/site-packages/openstack_dashboard/dashboards/theme:
  file.symlink:
  - target: /srv/horizon/sites/{{ app_name }}/plugins/{{ plugin_name }}/horizon_theme/dashboards/theme
  - user: root
  - group: root
  - require:
    - git: {{ app_name }}_{{ app.source.address }}

/srv/horizon/sites/{{ app_name }}/local/lib/python2.7/site-packages/openstack_dashboard/themes/{{ plugin.theme_name }}:
  file.symlink:
  - target: /srv/horizon/sites/{{ app_name }}/plugins/{{ plugin_name }}/horizon_theme/static/{{ plugin.theme_name }}
  - user: root
  - group: root
  - require:
    - git: {{ app_name }}_{{ app.source.address }}

{%- endif %}

{%- endfor %}

{%- endif %}

horizon_setup_{{ app_name }}:
  cmd.run:
  - names:
    - source /srv/horizon/sites/{{ app_name }}/bin/activate; python manage.py collectstatic --noinput; python manage.py compress --force
    {%- if app.plugin.merlin_panels is defined %}
    - source /srv/horizon/sites/{{ app_name }}/bin/activate; python manage.py syncdb --noinput
    {%- endif %}
    - chown horizon:horizon static -R
  - cwd: /srv/horizon/sites/{{ app_name }}
  - require:
    - file: /srv/horizon/sites/{{ app_name }}/manage.py
    - git: {{ app_name }}_{{ app.source.address }}
    {%- if app.get('version', 'juno') in ['juno'] %}
    - cmd: horizon_setup_{{ app_name }}_horizon
    {%- endif %}

/srv/horizon/sites/{{ app_name }}/gunicorn_start:
  file.managed:
  - source: salt://horizon/files/gunicorn_start
  - template: jinja
  - mode: 777
  - user: horizon
  - group: horizon
  - defaults:
    app_name: {{ app_name }}
  - require:
    - cmd: horizon_setup_{{ app_name }}

{%- endfor %}

{%- endif %}
