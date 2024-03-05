from extras.plugins import PluginMenuItem, PluginMenu, PluginMenuButton
from utilities.choices import ButtonColorChoices
from django.conf import settings
from django.utils.text import slugify

plugin_settings = settings.PLUGINS_CONFIG.get('netbox_rolesandgroups', {})


class MyPluginMenu(PluginMenu):
    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._name = name

    @property
    def name(self):
        return self._name


if plugin_settings.get('enable_navigation_menu'):

    menuitem = []

    # Add a menu item for system software if enabled
    if plugin_settings.get('enable_system_roles'):
        menuitem.append(
            PluginMenuItem(
                link='plugins:netbox_rolesandgroups:systemrole_list',
                link_text='Роли систем',
                buttons=[PluginMenuButton(
                    link='plugins:netbox_rolesandgroups:systemrole_add',
                    title='Создать',
                    icon_class='mdi mdi-plus-thick',
                    permissions=["netbox_rolesandgroups.change_systemrole"],
                    color=ButtonColorChoices.GREEN
                )],
                permissions=['netbox_rolesandgroups.view_systemrole']
            )
        )
    if plugin_settings.get('enable_system_rolegroups'):
        menuitem.append(
            PluginMenuItem(
                link='plugins:netbox_rolesandgroups:techrole_list',
                link_text='Технические роли АС',
                buttons=[PluginMenuButton(
                    link='plugins:netbox_rolesandgroups:techrole_add',
                    title='Создать',
                    icon_class='mdi mdi-plus-thick',
                    permissions=["netbox_rolesandgroups.change_systemrole"],
                    color=ButtonColorChoices.GREEN
                )],
                permissions=['netbox_rolesandgroups.view_systemrole']
            )
        )

    # If we are using NB 3.4.0+ display the new top level navigation option
    if settings.VERSION >= '3.4.0':
        menu = MyPluginMenu(
            name='rolesandgroupsPl',
            label='Роли систем',
            groups=(
                ('Роли систем', menuitem),
            ),
            icon_class='mdi mdi-account-group'
        )

    else:

        # Fall back to pre 3.4 navigation option
        menu_items = menuitem
