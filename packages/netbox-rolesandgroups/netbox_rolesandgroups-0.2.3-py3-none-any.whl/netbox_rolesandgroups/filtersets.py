from netbox.filtersets import NetBoxModelFilterSet
from .models import SystemRole, TechRole
from django.db.models import Q


class SystemRoleFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = SystemRole
        fields = ('id', 'name', 'slug', 'system', 'subsystems', 'parent', 'data_composition', 'upload_interface',
                  'upload_format', 'mapping_security_group', 'sed', 'link')

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(slug__icontains=value) |
            Q(description__icontains=value)
        )


class TechRoleFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = TechRole
        fields = ('id', 'name', 'slug', 'roles')

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(slug__icontains=value)
        )
