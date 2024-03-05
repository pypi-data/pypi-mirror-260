from extras.plugins import PluginTemplateExtension
from django.conf import settings
from .models import SystemRole, TechRole

plugin_settings = settings.PLUGINS_CONFIG.get('netbox_rolesandgroups', {})


class SystemRoleList(PluginTemplateExtension):
    model = 'netbox_subsystems.system'

    def full_width_page(self):
        if plugin_settings.get('enable_system_roles') and plugin_settings.get('system_roles_location') == 'full_width_page':
            systemroles = SystemRole.objects.filter(system=self.context['object'])
            techroles = TechRole.objects.filter(roles__in=[systemrole.id for systemrole in systemroles])
            return self.render('netbox_rolesandgroups/systemrole_include.html', extra_context={
                'system_roles': systemroles,
                'system_techroles': techroles
            })
        else:
            return ""

    def left_page(self):
        if plugin_settings.get('enable_system_roles') and plugin_settings.get('system_roles_location') == 'left':
            systemroles = SystemRole.objects.filter(system=self.context['object'])
            return self.render('netbox_rolesandgroups/systemrole_include.html', extra_context={
                'system_roles': systemroles,
            })
        else:
            return ""

    def right_page(self):
        if plugin_settings.get('enable_system_roles') and plugin_settings.get('system_roles_location') == 'right':
            systemroles = SystemRole.objects.filter(system=self.context['object'])
            return self.render('netbox_rolesandgroups/systemrole_include.html', extra_context={
                'system_roles': systemroles,
            })
        else:
            return ""


class SystemTechRoleList(PluginTemplateExtension):
    model = 'netbox_subsystems.system'

    def full_width_page(self):
        if plugin_settings.get('enable_system_techrole') and plugin_settings.get('system_techrole_location') == 'full_width_page':
            systemroles = SystemRole.objects.filter(system=self.context['object'])
            techroles = TechRole.objects.filter(roles__in=[systemrole.id for systemrole in systemroles])
            return self.render('netbox_rolesandgroups/systemtechrole_include.html', extra_context={
                'system_techroles': techroles,
            })
        else:
            return ""

    def left_page(self):
        if plugin_settings.get('enable_system_techrole') and plugin_settings.get('system_techrole_location') == 'left':
            systemroles = SystemRole.objects.filter(system=self.context['object'])
            techroles = TechRole.objects.filter(roles__in=[systemrole.id for systemrole in systemroles])
            return self.render('netbox_rolesandgroups/systemtechrole_include.html', extra_context={
                'system_techroles':  techroles,
            })
        else:
            return ""

    def right_page(self):
        if plugin_settings.get('enable_system_techrole') and plugin_settings.get('system_techrole_location') == 'right':
            systemroles = SystemRole.objects.filter(system=self.context['object'])
            techroles = TechRole.objects.filter(roles__in=[systemrole.id for systemrole in systemroles])
            return self.render('netbox_rolesandgroups/systemtechrole_include.html', extra_context={
                'system_techroles': techroles,
            })
        else:
            return ""


class SubsystemRoleList(PluginTemplateExtension):
    model = 'netbox_subsystems.subsystem'

    def full_width_page(self):
        if plugin_settings.get('enable_subsystem_role') and plugin_settings.get('subsystem_role_location') == 'full_width_page':
            systemroles = SystemRole.objects.filter(subsystems__in=[self.context['object']])
            # techroles = TechRole.objects.filter(roles__in=[systemrole.id for systemrole in systemroles])
            return self.render('netbox_rolesandgroups/subsystemrole_include.html', extra_context={
                'subsystem_roles': systemroles,
            })
        else:
            return ""

    def left_page(self):
        if plugin_settings.get('enable_subsystem_role') and plugin_settings.get('subsystem_role_location') == 'left':
            systemroles = SystemRole.objects.filter(subsystems__in=[self.context['object']])
            # techroles = TechRole.objects.filter(roles__in=[systemrole.id for systemrole in systemroles])
            return self.render('netbox_rolesandgroups/subsystemrole_include.html', extra_context={
                'subsystem_roles': systemroles,
            })
        else:
            return ""

    def right_page(self):
        if plugin_settings.get('enable_subsystem_role') and plugin_settings.get('subsystem_role_location') == 'right':
            systemroles = SystemRole.objects.filter(subsystems__in=[self.context['object']])
            # techroles = TechRole.objects.filter(roles__in=[systemrole.id for systemrole in systemroles])
            return self.render('netbox_rolesandgroups/subsystemrole_include.html', extra_context={
                'subsystem_roles': systemroles,
            })
        else:
            return ""


template_extensions = [SystemRoleList, SystemTechRoleList, SubsystemRoleList]
