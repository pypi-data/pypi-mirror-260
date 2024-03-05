from rest_framework import serializers

from netbox.api.serializers import NetBoxModelSerializer, WritableNestedSerializer
from netbox.api.fields import SerializedPKRelatedField
from ..models import SystemRole, TechRole
from netbox_subsystems.api.nested_serializers import NestedSystemSerializer, NestedSubsystemSerializer
from netbox_subsystems.models import Subsystem


# system Role Serializer
class NestedSystemRoleSerializer(WritableNestedSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_rolesandgroups-api:systemrole-detail'
    )

    class Meta:
        model = SystemRole
        fields = (
            'id', 'url', 'display', 'name', 'slug',
        )


class SystemRoleSerializer(NetBoxModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_rolesandgroups-api:systemrole-detail'
    )

    system = NestedSystemSerializer(required=False, allow_null=True)
    # subsystem = NestedSubsystemSerializer(required=False, allow_null=True)
    subsystems = SerializedPKRelatedField(
        queryset=Subsystem.objects.all(),
        serializer=NestedSubsystemSerializer,
        required=False,
        many=True
    )
    parent = NestedSystemRoleSerializer(required=False, allow_null=True)

    class Meta:
        model = SystemRole
        fields = (
            'id', 'url', 'display', 'name', 'slug', 'system', 'subsystems', 'parent', 'data_composition',
            'upload_interface', 'upload_format', 'mapping_security_group', 'sed', 'link', 'description', 'comments',
            'tags', 'custom_fields', 'created', 'last_updated',
        )


# system Role Group  Serializer
class TechRoleSerializer(NetBoxModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_rolesandgroups-api:techrole-detail'
    )
    roles = SerializedPKRelatedField(
        queryset=SystemRole.objects.all(),
        serializer=NestedSystemRoleSerializer,
        required=False,
        many=True
    )
    #roles = NestedSystemRoleSerializer(many=True, required=False)

    class Meta:
        model = TechRole
        fields = (
            'id', 'url', 'display', 'name', 'slug', 'roles', 'comments', 'tags',
            'custom_fields', 'created', 'last_updated',
        )


class NestedTechRoleSerializer(WritableNestedSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_rolesandgroups-api:techrole-detail'
    )

    class Meta:
        model = TechRole
        fields = (
            'id', 'url', 'display', 'name', 'slug',
        )

