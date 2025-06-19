# Automate with Ansible

## Hello IT. Did you try turning it on and off again?

**Mitanshu Sukhwani** • _09 June 2025_

I learned all about [ansible](https://docs.ansible.com/ansible/latest/getting_started/index.html), which automates the management of remote systems and controls their desired state, from this fantastic YouTube Channel - [LearnLinuxTV](https://www.youtube.com/@LearnLinuxTV).

[Here is the ansible playlist](https://youtube.com/playlist?list=PLT98CRl2KxKEUHie1m24-wkyHpEsa4Y70&feature=shared).

The idea with ansible is to have a certain set of rules, which we call Playbook, define how software gets installed on computer systems at scale.

![Ansible environment](https://docs.ansible.com/ansible/latest/_images/ansible_inv_start.svg)

On your Control Node, device from which you will be running the playbook, you can install Ansible as follows:

```bash
$ pipx install --include-deps ansible
```

Confirm your installation by:

```bash
$ ansible --version
```

The [Playbook](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_intro.html) is a simple [YAML](https://yaml.org/) file.

In an Ansible playbook, you can name your tasks, create groups for specific tasks, act as a specific user, and run the tasks needed to perform.

```yaml
- name: Update web servers
  hosts: webservers
  remote_user: root

  tasks:
    - name: Ensure apache is at the latest version
      ansible.builtin.yum:
        name: httpd
        state: latest
```

Best part about using ansible is idempotency. Most Ansible modules check whether the desired final state has already been achieved, and exit without performing any actions if that state has been achieved, so that repeating the task does not change the final state.

You can also protect you sensitive data with [Ansible vault](https://docs.ansible.com/ansible/latest/vault_guide/index.html). Vault encrypts your sensitive data so you dont have to store keys in plain text. While running the playbook, direct ansible to ask you for vault to decrypt the data before running:

```bash
ansible-playbook local.yml --ask-vault-pass --ask-become-pass
```

`--ask-become-pass` helps you perform tasks that require administrator privileges.

Find my ansible configuration at [mitanshu7/ansible_workstation](https://github.com/mitanshu7/ansible_workstation).

I highly recommend learning about ansible from the mentioned [YouTube Playlist](https://youtube.com/playlist?list=PLT98CRl2KxKEUHie1m24-wkyHpEsa4Y70&feature=shared).
