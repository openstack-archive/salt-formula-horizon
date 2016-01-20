# Add to installed apps
ADD_INSTALLED_APPS = ['horizon_network_allocation_panel']
# The slug of the panel to be added to HORIZON_CONFIG. Required.
PANEL = 'network_allocation'
# The slug of the dashboard the PANEL associated with. Required.
PANEL_DASHBOARD = 'admin'
# The slug of the panel group the PANEL is associated with.
PANEL_GROUP = 'admin'

# Python panel class of the PANEL to be added.
ADD_PANEL = 'horizon_network_allocation_panel.panel.NetworkAllocationPanel'
