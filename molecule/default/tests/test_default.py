import os

import testinfra.utils.ansible_runner

import re

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_consul_user(host):
    consul_user = host.user("consul")

    assert consul_user.exists
    assert consul_user.group == "consul"
    assert consul_user.shell == "/sbin/nologin"
    assert consul_user.home == "/var/run/consul"


def test_consul_bin(host):
    consul_bin = host.file('/usr/sbin/consul')

    assert consul_bin.exists
    assert consul_bin.is_file
    assert consul_bin.mode == 0o755


def test_consul_bin_ver(host):
    consul_bin_ver = host.check_output('/usr/sbin/consul --version')
    assert re.match("^Consul v1.8.4", consul_bin_ver)


def test_consul_conf_dir(host):
    consul_conf_dir = host.file('/etc/consul')

    assert consul_conf_dir.exists
    assert consul_conf_dir.mode == 0o755
    assert consul_conf_dir.is_directory


def test_consul_config(host):
    consul_config = host.file('/etc/consul/consul.hcl')

    assert consul_config.exists
    assert consul_config.is_file
    assert consul_config.user == 'consul'
    assert consul_config.group == 'consul'
    assert consul_config.mode == 0o640


def test_consul_gossip_config(host):
    consul_gossip_config = host.file('/etc/consul/gossip-encryption.json')

    assert consul_gossip_config.exists
    assert consul_gossip_config.is_file
    assert consul_gossip_config.user == 'consul'
    assert consul_gossip_config.group == 'consul'
    assert consul_gossip_config.mode == 0o400


def test_consul_confd_dir(host):
    consul_confd_dir = host.file('/etc/consul/conf.d')

    assert consul_confd_dir.exists
    assert consul_confd_dir.is_directory
    assert consul_confd_dir.user == 'consul'
    assert consul_confd_dir.group == 'consul'
    assert consul_confd_dir.mode == 0o755


def test_consul_sys_defaults(host):
    if host.system_info.distribution == "centos":
        defaults = "/etc/sysconfig/consul"
    elif host.system_info.distribution == "debian":
        defaults = "/etc/default/consul"

        consul_sys_defaults = host(defaults)
        assert consul_sys_defaults.exists
        assert consul_sys_defaults.is_file
        assert consul_sys_defaults.mode == 0o600


def test_consul_data_dir(host):
    consul_data_dir = host.file('/var/lib/consul')

    assert consul_data_dir.exists
    assert consul_data_dir.is_directory
    assert consul_data_dir.mode == 0o755


def test_consul_run_dir(host):
    consul_run_dir = host.file('/var/run/consul')

    assert consul_run_dir.exists
    assert consul_run_dir.is_directory


def test_consul_systemd_file(host):
    consul_systemd_file = host.file('/lib/systemd/system/consul.service')

    assert consul_systemd_file.exists
    assert consul_systemd_file.is_file
    assert consul_systemd_file.mode == 0o666


def test_consul_running_and_enabled(host):
    consul_service = host.service('consul')

    assert consul_service.is_running
    assert consul_service.is_enabled
