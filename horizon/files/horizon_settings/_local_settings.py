{%- from "horizon/map.jinja" import server with context %}

{%- if server.app is defined %}
{%- set app = salt['pillar.get']('horizon:server:app:'+app_name) %}
{%- else %}
{%- set app = salt['pillar.get']('horizon:server') %}
{%- endif %}

DEBUG = {% if app.get('development', False) %}True{% else %}False{% endif %}

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']

{%- if app.ssl is defined %}
{%- if app.ssl.enabled %}
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
{%- endif %}
{%- endif %}

AUTHENTICATION_URLS = ['openstack_auth.urls']

LOCAL_PATH = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = '{{ app.secret_key }}'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        {%- if app.cache.members is defined %}
        'LOCATION': "{%- for member in app.cache.members %}{{ member.host }}:{{ member.port }}{% if not loop.last %};{% endif %}{%- endfor %}"
        {%- else %}
        'LOCATION': '{{ app.cache.host }}:{{ app.cache.port }}',
        {%- endif %}
    }
}

# Send email to the console by default
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# Or send them to /dev/null
#EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

# Configure these for your outgoing email host
# EMAIL_HOST = 'smtp.my-company.com'
# EMAIL_PORT = 25
# EMAIL_HOST_USER = 'djangomail'
# EMAIL_HOST_PASSWORD = 'top-secret!'

# The number of objects (Swift containers/objects or images) to display
# on a single page before providing a paging element (a "more" link)
# to paginate results.
API_RESULT_LIMIT = 1000
API_RESULT_PAGE_SIZE = 20

# The timezone of the server. This should correspond with the timezone
# of your entire OpenStack installation, and hopefully be in UTC.
TIME_ZONE = "UTC"

COMPRESS_OFFLINE = True

# Trove user and database extension support. By default support for
# creating users and databases on database instances is turned on.
# To disable these extensions set the permission here to something
# unusable such as ["!"].
# TROVE_ADD_USER_PERMS = []
# TROVE_ADD_DATABASE_PERMS = []

{%- if app.uenc_api is defined %}
UENC_HOST = '{{ app.uenc_api.host }}'
UENC_PORT = '{{ app.uenc_api.port }}'
{%- endif %}

{%- if app.control_nodes is defined %}
OPENSTACK_CONTROL_NODES = {{ app.control_nodes|python }}
{%- endif %}

{%- if app.sensu_api is defined %}
{%- if app.sensu_api.host is defined %}
SENSU_HOST = '{{ app.sensu_api.host }}'
SENSU_PORT = '{{ app.sensu_api.port }}'
{%- else %}
SENSU_API = {{ app.sensu_api|python }}
def check_filter(check):
    return ":".join(check['name'].split("_")[1:-1])
SENSU_CHECK_FILTER = check_filter
{%- endif %}
{%- endif %}

{%- if app.kedb_api is defined %}
KEDB_HOST = '{{ app.kedb_api.host }}'
KEDB_PORT = '{{ app.kedb_api.port }}'
{%- endif %}

{%- if app.cold_api is defined %}
COLD_HOST = '{{ app.cold_api.host }}'
COLD_PORT = '{{ app.cold_api.port }}'
{%- endif %}

{%- if app.robotice_api is defined %}
ROBOTICE_HOST = '{{ app.robotice_api.host }}'
ROBOTICE_PORT = '{{ app.robotice_api.port }}'
{%- endif %}

{%- if app.csb_api is defined %}
CSB_HOST = '{{ app.csb_api.host }}'
CSB_PORT = '{{ app.csb_api.port }}'
AUTHENTICATION_BACKENDS = ('csb_auth.backend.CSBackend',)
{%- endif %}

{%- if app.murano_api is defined %}
MURANO_API_URL = "http://{{ app.murano_api.host }}:{{ app.murano_api.port }}"
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
# TODO(majklk) make this configurable
MURANO_REPO_URL = 'http://storage.apps.openstack.org/'
# this folder muset exists before start
#METADATA_CACHE_DIR = '/var/cache/muranodashboard-cache'
{%- endif %}

{%- if app.helpdesk_api is defined %}
HELPDESK_HOST = '{{ app.helpdesk_api.host }}'
HELPDESK_PORT = '{{ app.helpdesk_api.port }}'
{%- endif %}

{%- for plugin_name, plugin in app.get('plugin', {}).iteritems() %}

{%- if plugin.database is defined %}
{%- set db = plugin.database %}
RALLY_DB = "{{ db.engine }}://{{ db.username }}:{{ db.password }}@{{ db.get('host', '127.0.0.1') }}/{{ db.name }}"
{%- endif %}

{%- if plugin.override is defined %}
HORIZON_CONFIG['customization_module'] = '{{ plugin.app }}.overrides'
{%- endif %}

{%- if plugin.mask_url is defined %}
API_MASK_URL = '{{ plugin.mask_url }}'
{%- endif %}

{%- if plugin.config is defined %}
{{ plugin_name|upper }}_CONFIG = {{ plugin.config|python }}
{%- endif %}

{%- if plugin.mask_protocol is defined %}
API_MASK_PROTOCOL = '{{ plugin.mask_protocol }}'
{%- endif %}

{%- if plugin.metric is defined %}
{%- if plugin.metric.engine == "graphite" %}
GRAPHITE_HOST = "{{ plugin.metric.host }}"
GRAPHITE_PORT = "{{ plugin.metric.port }}"
GRAPHITE_ENDPOINT = 'http://%s:%s/' % (GRAPHITE_HOST, GRAPHITE_PORT)
{%- endif %}
{%- endif %}

{%- if plugin.overrides is defined %}
OVERRIDES = (
    {%- for override in plugin.overrides %}
    "{{ override }}",
    {%- endfor %}
)
{%- endif %}

{%- if plugin_name == "sahara" %}
SAHARA_USE_NEUTRON = True
AUTO_ASSIGNMENT_ENABLED = False
{%- endif %}

{%- if plugin_name == "contrail" and app.get("version", "juno") == "juno" %}
from openstack_dashboard.settings import STATICFILES_DIRS
import xstatic
from contrail_openstack_dashboard.openstack_dashboard.xstatic.pkg import contrail

pkg = __import__('contrail_openstack_dashboard.openstack_dashboard')

STATICFILES_DIRS.append(('dashboard/js/', xstatic.main.XStatic(contrail).base_dir))

{%- endif %}

{%- if plugin.urls is defined %}
AUTHENTICATION_URLS += {{ plugin.urls|python }}
{%- endif %}

{%- endfor %}

{%- if app.logging is defined %}
RAVEN_CONFIG = {
    'dsn': '{{ app.logging.dsn }}',
}
{%- endif %}

SITE_BRANDING = '{{ app.get('branding', 'OpenStack Dashboard') }}'
