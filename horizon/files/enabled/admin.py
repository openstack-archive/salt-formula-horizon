
ENABLED = {{enabled | python}}

{%- if enabled %}

DASHBOARD = 'admin'

# A list of applications to be added to INSTALLED_APPS.
ADD_INSTALLED_APPS = [
    'openstack_dashboard.dashboards.admin',
]

{%- endif %}
