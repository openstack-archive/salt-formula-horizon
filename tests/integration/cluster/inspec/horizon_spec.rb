





# TODO, enable helper files once resolved - https://github.com/chef/kitchen-inspec/issues/93
#require 'spec_helper'
param = {
  user: 'horizon',
  group: 'horizon',
}

# based on operating system we select the available service
if ['centos', 'fedora', 'freebsd', 'opensuse'].include?(os[:family])
  # CentOS, Fedora
  service_nm = 'httpd'
  config = '/etc/openstack-dashboard/local_settings'
  apache_config = '/etc/httpd/conf.d/openstack-dashboard.conf'
elsif ['debian', 'ubuntu'].include?(os[:family])
  # Debian, Ubuntu
  service_nm = 'apache'
  config = '/etc/openstack-dashboard/local_settings.py'
  apache_config = '/etc/apache2/conf-available/openstack-dashboard.conf'
end

control 'horizon' do

  # TODO, check for config files and content
   #debian
  #'config': '/etc/openstack-dashboard/local_settings.py',
  #'apache_config': '/etc/apache2/conf-available/openstack-dashboard.conf',
  #'port_config_file': '/etc/apache2/ports.conf',
  #'port_config_template': 'salt://horizon/files/ports.conf',
   #rhel
  #'config': '/etc/openstack-dashboard/local_settings',
  #'apache_config': '/etc/httpd/conf.d/openstack-dashboard.conf',
  #'port_config_file': '/etc/httpd/conf/httpd.conf',
  #'port_config_template': 'salt://horizon/files/httpd.conf',


  describe file(config) do
    it { should exist }
    its('content') { should match("SECRET_KEY = 'secret'") }
    #it { should be_owned_by param[:user] }
    #it { should be_grouped_into param[:group] }
  end
end

control 'apache config' do
  describe file(apache_config) do
    it { should exist }
    its('content') { should match("WSGIDaemonProcess horizon user=horizon group=horizon") }
  end
end


return
return if ENV['DOCKER']

#control 'web server' do

  #if os[:family] == 'ubuntu' && os[:release] >= '16.04'
    #describe systemd_service(service_nm) do
      #it { should be_enabled }
      #it { should be_installed }
      #it { should be_running }
    #end
  #else
    #describe_service(service_nm) do
      #it { should be_enabled }
      #it { should be_installed }
      #it { should be_running }
    #end
  #end


  #if os.unix?
    #describe port(80) do
      #it { should be_listening }
      #its('protocols') { should include('tcp') }
    #end

  #end
#end


