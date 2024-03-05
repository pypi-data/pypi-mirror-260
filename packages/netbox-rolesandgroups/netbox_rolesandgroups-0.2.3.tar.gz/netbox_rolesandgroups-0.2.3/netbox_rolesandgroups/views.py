from django.contrib.auth.mixins import PermissionRequiredMixin
from netbox.views import generic
from utilities.views import register_model_view
from . import forms, models, tables, filtersets
from netbox_subsystems.tables import SubsystemTable


### SystemRole
@register_model_view(models.SystemRole)
class SystemRoleView(PermissionRequiredMixin, generic.ObjectView):
    permission_required = "netbox_rolesandgroups.view_systemrole"
    queryset = models.SystemRole.objects.all()

    def get_extra_context(self, request, instance):
        techrole_table = tables.TechRoleTable(models.TechRole.objects.filter(roles=instance))
        techrole_table.configure(request)
        subsystem_table = SubsystemTable(instance.subsystems.all())
        subsystem_table.configure(request)
        return {
            'techrole_table': techrole_table,
            'subsystem_table': subsystem_table,
        }


class SystemRoleListView(PermissionRequiredMixin, generic.ObjectListView):
    permission_required = "netbox_rolesandgroups.view_systemrole"
    queryset = models.SystemRole.objects.all()
    table = tables.SystemRoleTable
    filterset = filtersets.SystemRoleFilterSet
    filterset_form = forms.SystemRoleFilterForm


@register_model_view(models.SystemRole, 'edit')
class SystemRoleEditView(PermissionRequiredMixin, generic.ObjectEditView):
    permission_required = "netbox_rolesandgroups.change_systemrole"
    queryset = models.SystemRole.objects.prefetch_related('subsystems', 'tags')
    form = forms.SystemRoleForm
    template_name = 'netbox_rolesandgroups/systemrole_edit.html'


@register_model_view(models.SystemRole, 'delete')
class SystemRoleDeleteView(PermissionRequiredMixin, generic.ObjectDeleteView):
    permission_required = "netbox_rolesandgroups.delete_systemrole"
    queryset = models.SystemRole.objects.all()


class SystemRoleBulkImportView(generic.BulkImportView):
    permission_required = "netbox_rolesandgroups.view_systemrole"
    queryset = models.SystemRole.objects.all()
    model_form = forms.SystemRoleImportForm


class SystemRoleBulkEditView(generic.BulkEditView):
    permission_required = "netbox_rolesandgroups.change_systemrole"
    queryset = models.SystemRole.objects.all()
    filterset = filtersets.SystemRoleFilterSet
    table = tables.SystemRoleTable
    form = forms.SystemRoleBulkEditForm


class SystemRoleBulkDeleteView(generic.BulkDeleteView):
    permission_required = "netbox_rolesandgroups.delete_systemrole"
    queryset = models.SystemRole.objects.all()
    filterset = filtersets.SystemRoleFilterSet
    table = tables.SystemRoleTable


### TechRole
@register_model_view(models.TechRole)
class TechRoleView(PermissionRequiredMixin, generic.ObjectView):
    permission_required = "netbox_rolesandgroups.view_systemrole"
    queryset = models.TechRole.objects.all()

    def get_extra_context(self, request, instance):
        table = tables.SystemRoleTable(instance.roles.all())
        table.configure(request)
        return {
            'systemrole_table': table,
        }


class TechRoleListView(PermissionRequiredMixin, generic.ObjectListView):
    permission_required = "netbox_rolesandgroups.view_systemrole"
    queryset = models.TechRole.objects.all()
    table = tables.TechRoleTable
    filterset = filtersets.TechRoleFilterSet
    filterset_form = forms.TechRoleFilterForm


@register_model_view(models.TechRole, 'edit')
class TechRoleEditView(PermissionRequiredMixin, generic.ObjectEditView):
    permission_required = "netbox_rolesandgroups.change_systemrole"
    queryset = models.TechRole.objects.all()
    form = forms.TechRoleForm

    template_name = 'netbox_rolesandgroups/techrole_edit.html'


@register_model_view(models.TechRole, 'delete')
class TechRoleDeleteView(PermissionRequiredMixin, generic.ObjectDeleteView):
    permission_required = "netbox_rolesandgroups.delete_systemrole"
    queryset = models.TechRole.objects.all()


class TechRoleBulkImportView(generic.BulkImportView):
    permission_required = "netbox_rolesandgroups.view_systemrole"
    queryset = models.TechRole.objects.all()
    model_form = forms.TechRoleImportForm


class TechRoleBulkEditView(generic.BulkEditView):
    permission_required = "netbox_rolesandgroups.change_systemrole"
    queryset = models.TechRole.objects.all()
    filterset = filtersets.TechRoleFilterSet
    table = tables.TechRoleTable
    form = forms.TechRoleBulkEditForm


class TechRoleBulkDeleteView(generic.BulkDeleteView):
    permission_required = "netbox_rolesandgroups.delete_systemrole"
    queryset = models.TechRole.objects.all()
    filterset = filtersets.TechRoleFilterSet
    table = tables.TechRoleTable
