{%- from "horizon/map.jinja" import server with context %}

{%- if server.app is defined %}
{%- set app = salt['pillar.get']('horizon:server:app:'+app_name) %}
{%- else %}
{%- set app = salt['pillar.get']('horizon:server') %}
{%- endif %}

# Set Console type:
# valid options would be "AUTO", "VNC" or "SPICE"
# CONSOLE_TYPE = "AUTO"

# The Xen Hypervisor has the ability to set the mount point for volumes
# attached to instances (other Hypervisors currently do not). Setting
# can_set_mount_point to True will add the option to set the mount point
# from the UI.
OPENSTACK_HYPERVISOR_FEATURES = {
    'can_set_mount_point': False,
    'can_set_password': False,
}

# When launching an instance, the menu of available flavors is
# sorted by RAM usage, ascending.  Provide a callback method here
# (and/or a flag for reverse sort) for the sorted() method if you'd
# like a different behaviour.  For more info, see
# http://docs.python.org/2/library/functions.html#sorted
# CREATE_INSTANCE_FLAVOR_SORT = {
#     'key': my_awesome_callback_method,
#     'reverse': False,
# }

FLAVOR_EXTRA_KEYS = {
    'flavor_keys': [
        ('quota:read_bytes_sec', _('Quota: Read bytes')),
        ('quota:write_bytes_sec', _('Quota: Write bytes')),
        ('quota:cpu_quota', _('Quota: CPU')),
        ('quota:cpu_period', _('Quota: CPU period')),
        ('quota:inbound_average', _('Quota: Inbound average')),
        ('quota:outbound_average', _('Quota: Outbound average')),
    ]
}
