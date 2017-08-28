# -*- mode: ruby -*-
# vi: set ft=ruby :
require 'json'
# Number of VMs to start
N = 1
# Qdrouterd confs
CONFS_PATH = "generated/complete_3_1/confs.json"
CONFS = JSON.parse(File.read(CONFS_PATH))

$rabbit = <<SCRIPT
apt-get install -y rabbitmq-server
rabbitmqctl add_user test test
rabbitmqctl set_permissions -p / test ".*" ".*" ".*"
service rabbitmq-server restart
SCRIPT

$all = <<SCRIPT
apt-get update
apt-get install -y python-dev python-pip
pip install -U pip
pip install -r /vagrant/requirements.txt
SCRIPT

Vagrant.configure(2) do |config|
  config.vm.box = 'boxcutter/ubuntu1604'
  config.ssh.insert_key = false
  config.vm.synced_folder ".", "/vagrant", type: "rsync", disabled: false
  config.hostmanager.ignore_private_ip = true
  config.hostmanager.enabled = true
  config.hostmanager.manage_guest = true

	config.vm.provider "g5k" do |g5k, override|
		override.nfs.functional = false
		g5k.project_id = "test-vagrant-g5k"
		g5k.site = "nancy"
		g5k.username = "msimonin"
		g5k.gateway = "access.grid5000.fr"
		g5k.walltime = "03:00:00"
		g5k.image = {
			:path    => "/home/msimonin/public/ubuntu-16.04.qcow2",
			:backing => "snapshot"
		}
		g5k.net = {
			:type => "bridge",
#            :ports => ["#{2222+i}-:22"]
		}
		g5k.oar = "virtual != 'none'"
#		g5k.resources = {
#			:cpu => 1,
#			:mem => 2048
#		}
	end #g5k

  (0..N-1).each do |i|
    config.vm.define "machine#{i}" do |machine|
      machine.vm.network "private_network", ip: "192.168.11.#{2 + i}"
      if i == N - 1
        config.vm.provision "ansible" do |ansible|
          ansible.limit = "all"
          ansible.playbook = "main.yml"
          ansible.extra_vars = CONFS
        end
      end
    end
  end

end
