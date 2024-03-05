from extras.plugins import PluginConfig


class NetboxRolesAndGroupse(PluginConfig):
    name = 'netbox_rolesandgroups'
    verbose_name = 'Роли систем'
    description = 'Manage rolesandgroups for systems in Netbox'
    version = '0.1.1'
    author = 'Ilya Zakharov'
    author_email = 'ilya.zakharov@domrf.ru'
    min_version = '3.2.0'
    base_url = 'rolesandgroups'
    default_settings = {
        "enable_navigation_menu": True,
        "enable_system_roles": True,
        "enable_system_rolegroups": True,
        "system_roles_location": "left",
        "system_rolegroups_location": "left",
    }


config = NetboxRolesAndGroupse
