# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "puppetlabs/debian-7.4-64-puppet"

  config.vm.network :forwarded_port, guest: 80, host: 8080
  config.vm.network :forwarded_port, guest: 8000, host: 8000
  config.vm.network :forwarded_port, guest: 1080, host: 1080

  config.vm.synced_folder ".", "/var/www/dymmer", create: true

  config.vm.provision :shell do |shell|
    shell.inline = "mkdir -p /etc/puppet/modules;
                    apt-get update; apt-get install -y ca-certificates;
                    puppet module install --force puppetlabs/postgresql;
                    puppet module install --force puppetlabs/mysql;
                    puppet module install --force puppetlabs/stdlib;
                    puppet module install --force puppetlabs/apt;
                    puppet module install --force ripienaar/concat;
                    puppet module install --force stankevich-python;
                    puppet module install --force puppetlabs-apache;
                    puppet module install --force actionjack-mailcatcher"
  end

  config.vm.provision :puppet do |puppet|
    puppet.manifests_path = "manifests"
    puppet.manifest_file  = "dymmer.pp"
  end

end
