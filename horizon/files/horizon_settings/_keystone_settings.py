{%- from "horizon/map.jinja" import server with context %}

{%- if server.app is defined %}
{%- set app = salt['pillar.get']('horizon:server:app:'+app_name) %}
{%- else %}
{%- set app = salt['pillar.get']('horizon:server') %}
{%- endif %}

# Overrides for OpenStack API versions. Use this setting to force the
# OpenStack dashboard to use a specfic API version for a given service API.
# NOTE: The version should be formatted as it appears in the URL for the
# service API. For example, The identity service APIs have inconsistent
# use of the decimal point, so valid options would be "2.0" or "3".
{%- if app.api_versions is defined %}
OPENSTACK_API_VERSIONS = {
{%- for key, value in app.api_versions.iteritems() %}
    "{{ key }}": {{ value }}{% if not loop.last %},{% endif %}
{%- endfor %}
}
{%- endif %}
# Set this to True if running on multi-domain model. When this is enabled, it
# will require user to enter the Domain name in addition to username for login.
# OPENSTACK_KEYSTONE_MULTIDOMAIN_SUPPORT = False

# Overrides the default domain used when running on single-domain model
# with Keystone V3. All entities will be created in the default domain.
# OPENSTACK_KEYSTONE_DEFAULT_DOMAIN = 'Default'

{%- if app.regions is defined %}
AVAILABLE_REGIONS = [
{% for region in app.regions -%}
    ('{{ region.api }}','{{ region.name }}')
    {%- if not loop.last -%},{%- endif -%}
{%- endfor -%}
]
{%- endif %}


OPENSTACK_HOST = "{{ app.identity.host }}"
{%- if app.get('api_versions', {}).identity is defined %}
OPENSTACK_KEYSTONE_URL = "http{% if app.identity.encryption == 'ssl' %}s{% endif %}://%s:{{ app.identity.port }}/v{{ app.api_versions.identity }}" % OPENSTACK_HOST
{%- else %}
OPENSTACK_KEYSTONE_URL = "http{% if app.identity.encryption == 'ssl' %}s{% endif %}://%s:{{ app.identity.port }}/v2.0" % OPENSTACK_HOST
{%- endif %}

{%- if app.get('multidomain', false) %}
OPENSTACK_KEYSTONE_MULTIDOMAIN_SUPPORT = True
OPENSTACK_KEYSTONE_DEFAULT_DOMAIN = 'default'
{%- endif %}

OPENSTACK_KEYSTONE_DEFAULT_ROLE = "Member"

# Disable SSL certificate checks (useful for self-signed certificates):
{%- if app.identity.encryption == 'ssl' %}
OPENSTACK_SSL_NO_VERIFY = True
{%- endif %}

# The CA certificate to use to verify SSL connections
# OPENSTACK_SSL_CACERT = '/path/to/cacert.pem'

# OPENSTACK_ENDPOINT_TYPE specifies the endpoint type to use for the endpoints
# in the Keystone service catalog. Use this setting when Horizon is running
# external to the OpenStack environment. The default is 'publicURL'.
OPENSTACK_ENDPOINT_TYPE = "publicURL"

# SECONDARY_ENDPOINT_TYPE specifies the fallback endpoint type to use in the
# case that OPENSTACK_ENDPOINT_TYPE is not present in the endpoints
# in the Keystone service catalog. Use this setting when Horizon is running
# external to the OpenStack environment. The default is None.  This
# value should differ from OPENSTACK_ENDPOINT_TYPE if used.
#SECONDARY_ENDPOINT_TYPE = "publicURL"

# The OPENSTACK_KEYSTONE_BACKEND settings can be used to identify the
# capabilities of the auth backend for Keystone.
# If Keystone has been configured to use LDAP as the auth backend then set
# can_edit_user to False and name to 'ldap'.
#
# TODO(tres): Remove these once Keystone has an API to identify auth backend.
OPENSTACK_KEYSTONE_BACKEND = {
    'name': 'native',
    'can_edit_user': True,
    'can_edit_group': True,
    'can_edit_project': True,
    'can_edit_domain': True,
    'can_edit_role': True
}
