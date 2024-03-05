# Netbox Roles And Groups Plugin

A plugin designed to faciliate the storage of site, circuit, device type and device specific software within [NetBox](https://github.com/netbox-community/netbox)

## Compatibility

| NetBox Version | Plugin Version |
|----------------|----------------|
|     3.2+       |      0.5.0     |


## Installation

A working installation of Netbox 3.2+ is required. 3.4+ is recommended.

#### Package Installation from PyPi

Activate your virtual env and install via pip:

```
$ source /opt/netbox/venv/bin/activate
(venv) $ pip install netbox-rolesandgroups
```

To ensure the Netbox software plugin is automatically re-installed during future upgrades, add the package to your `local_requirements.txt` :

```no-highlight
# echo netbox-rolesandgroups >> local_requirements.txt
```

#### Enable the Plugin

In the Netbox `configuration.py` configuration file add or update the PLUGINS parameter, adding `netbox-rolesandgroups`:

```python
PLUGINS = [
    'netbox-rolesandgroups',
]
```

(Optional) Add or update a PLUGINS_CONFIG parameter in `configuration.py` to configure plugin settings. Options shown below are the configured defaults:

```python
PLUGINS_CONFIG = {
    'netbox-rolesandgroups': {
        "enable_navigation_menu": True,
        "enable_system_roles": True,
        "enable_system_rolegroups": True,
        "system_roles_location": "left",
        "system_rolegroups_location": "left",
    }
}

```

#### Apply Database Migrations

Apply database migrations with Netbox `manage.py`:

```
(venv) $ python manage.py migrate
```

#### Restart Netbox

Restart the Netbox service to apply changes:

```
sudo systemctl restart netbox
```

#### Re-index Netbox search index (Upgrade to 3.4 only)

If you are upgrading from Netbox 3.2 or above to Netbox 3.4, any previously inserted software may not show up in the new search feature. To resolve this, re-index the plugin:

```
(venv) $ python manage.py reindex netbox-rolesandgroups
```

