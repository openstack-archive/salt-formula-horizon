{%- from "horizon/map.jinja" import server with context %}
{%- set app = salt['pillar.get']('horizon:server:app:'+app_name) %}

ALLOWED_HOSTS = ['*']

{%- if app.ssl is defined %}
{%- if app.ssl.enabled %}
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
{%- endif %}
{%- endif %}

SECRET_KEY = '{{ app.secret_key }}'

{% include "horizon/files/local_settings/_keystone_settings.py" %}

{%- if app.plugin.merlin_panels is defined %}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/srv/horizon/sites/{{ app_name }}/database.db',
        'TEST_NAME': 'test_db:', 
    }
}

{%- endif %}
