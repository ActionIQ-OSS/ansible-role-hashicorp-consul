# ansible-role-hashicorp-consul

[![Build Status](https://github.com/OldCrowEW/ansible-role-hashicorp-consul/actions/workflows/molecule.yml/badge.svg?branch=master)](https://github.com/OldCrowEW/ansible-role-hashicorp-consul/actions)

Consul is a distributed service mesh to connect, secure, and configure services across any runtime platform and public
or private cloud.

This role deploys one node with bootstrap, server and ui role(s).

## Requirements

You must have the unzip package installed on target machine for unarchive task to complete successfully.

## Role Variables

So many vars. Var all the things! Although this role only currently supports CentOS 7 & Ubuntu 18, it can easily be used on say a
raspberry pi by having a playbook such as:

    - hosts: consul
      become: yes

      vars:
        consul_arch: arm
        consul_sysconfig: /etc/default/consul
      roles:
         - ansible-role-hashicorp-consul

## Dependencies

None.

## Example Playbook

    - hosts: servers
      roles:
         - { role: ansible-role-hashicorp-consul }

Slightly more complex server and client

    - name: install the consul service as a server
      hosts: consul-server
      roles:
      - role: consul
        consul_user: "ubuntu"
        consul_group: "ubuntu"
        consul_user_is_system: "false"
        consul_run_dir: "/home/ubuntu"
        consul_user_shell: "/bin/bash"
        consul_version: "1.5.3"
        consul_command_opts: "-server -bootstrap -ui"
        consul_wan_join_addr: "consul-server.example-site2.com"
        consul_lan_join_addr: "consul-server.example.com"
        consul_systemd_enabled: "false"
        consul_datacenter: "dc1"

    - name: install the consul service as an agent on all other machines
      hosts: clients
      roles:
      - role: consul
        consul_user: "ubuntu"
        consul_group: "ubuntu"
        consul_user_is_system: "false"
        consul_run_dir: "/home/ubuntu"
        consul_user_shell: "/bin/bash"
        consul_version: "1.5.3"
        consul_command_opts: ""
        consul_lan_join_addr: "consul-server.example.com"
        consul_systemd_enabled: "false"
        consul_datacenter: "dc1"

Playbook to trigger client join for Consul Servers deployed from [Terraform AWS Consul](https://github.com/hashicorp/terraform-aws-consul/)

    - name: Install Hashicorp Consul Client role
      hosts: clients
      roles:
      - role: consul
        consul_command_opts: ""
        consul_start_join_enabled: "false"
        consul_retry_join_enabled: "true"
        consul_datacenter: "us-east-1"

## License

BSD

## Author Information

John Favorite