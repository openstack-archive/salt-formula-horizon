# The slug of the panel to be added to HORIZON_CONFIG. Required.
PANEL = '{{ panel_name }}'
# The slug of the dashboard the PANEL associated with. Required.
PANEL_DASHBOARD = '{{ panel.get("dashboard") }}'
# The slug of the panel group the PANEL is associated with.
PANEL_GROUP = '{{ panel.get("group") }}'

{%- if panel.get("enabled", True) %}

ADD_PANEL = '{{ panel.get("class") }}'
{%- else %}

REMOVE_PANEL = True
{%- endif %}

