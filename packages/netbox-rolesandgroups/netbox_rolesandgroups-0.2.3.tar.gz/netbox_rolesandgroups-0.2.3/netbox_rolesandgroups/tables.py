import django_tables2 as tables

from netbox.tables import NetBoxTable, columns
from .models import SystemRole, TechRole


SYSTEMROLE_LINK = """
{% if record %}
    <a href="{% url 'plugins:netbox_rolesandgroups:systemrole' pk=record.pk %}">{% firstof record.name record.name %}</a>
{% endif %}
"""

TECHROLE_LINK = """
{% if record %}
    <a href="{% url 'plugins:netbox_rolesandgroups:techrole' pk=record.pk %}">{% firstof record.name record.name %}</a>
{% endif %}
"""


class SystemRoleTable(NetBoxTable):
    name = tables.TemplateColumn(template_code=SYSTEMROLE_LINK)
    system = tables.Column(
        linkify=True
    )

    subsystems = columns.ManyToManyColumn(
        linkify_item=True
    )
    parent = tables.Column(
        linkify=True
    )

    tags = columns.TagColumn(
        url_name='plugins:netbox_rolesandgroups:systemrole_list'
    )

    class Meta(NetBoxTable.Meta):
        model = SystemRole
        fields = ('pk', 'id', 'name', 'system', 'subsystems', 'parent', 'data_composition',
                  'upload_interface', 'upload_format',
                  'mapping_security_group', 'sed', 'link', 'description', 'slug', 'comments', 'actions',
                  'created', 'last_updated', 'tags')
        default_columns = ('name', 'system', 'tags')


class TechRoleTable(NetBoxTable):
    name = tables.TemplateColumn(template_code=TECHROLE_LINK)
    roles = columns.ManyToManyColumn(
        linkify_item=True,
        verbose_name=' В составе ролей'
    )
    tags = columns.TagColumn(
        url_name='plugins:netbox_rolesandgroups:techrole_list'
    )

    class Meta(NetBoxTable.Meta):
        model = TechRole
        fields = ('pk', 'id', 'name', 'roles', 'slug', 'comments', 'actions',
                  'created', 'last_updated', 'tags')
        default_columns = ('name', 'roles', 'tags')
