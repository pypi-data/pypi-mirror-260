from netbox.api.viewsets import NetBoxModelViewSet

from .. import models, filtersets
from .serializers import SystemRoleSerializer, TechRoleSerializer


class SystemRoleViewSet(NetBoxModelViewSet):
    queryset = models.SystemRole.objects.prefetch_related('subsystems', 'tags')
    serializer_class = SystemRoleSerializer
    filterset_class = filtersets.SystemRoleFilterSet


class TechRoleViewSet(NetBoxModelViewSet):
    queryset = models.TechRole.objects.prefetch_related(
        'roles',
        'tags'
    )
    serializer_class = TechRoleSerializer
    filterset_class = filtersets.TechRoleFilterSet
