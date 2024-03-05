from django import forms
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm, NetBoxModelBulkEditForm, NetBoxModelImportForm
from utilities.forms.fields import CSVModelChoiceField
from .models import SystemRole, TechRole

from django.conf import settings
from packaging import version
from netbox_subsystems.models import System, Subsystem

NETBOX_CURRENT_VERSION = version.parse(settings.VERSION)
if NETBOX_CURRENT_VERSION >= version.parse("3.5"):
    from utilities.forms.fields import TagFilterField, CommentField, DynamicModelChoiceField, DynamicModelMultipleChoiceField, SlugField
else:
    from utilities.forms import TagFilterField, CommentField, DynamicModelChoiceField, DynamicModelMultipleChoiceField, SlugField


# system Role Form & Filter Form
class SystemRoleForm(NetBoxModelForm):
    comments = CommentField()

    system = DynamicModelChoiceField(
        label='Система',
        queryset=System.objects.all(),
        required=False,
        null_option='None'
    )
    subsystems = DynamicModelMultipleChoiceField(
        label='Подсистемы',
        queryset=Subsystem.objects.all()
    )

    parent = DynamicModelChoiceField(
        label='В составе роли',
        queryset=SystemRole.objects.all(),
        required=False,
        null_option='None'
    )
    slug = SlugField()

    class Meta:
        model = SystemRole
        fields = ('name', 'slug', 'system', 'subsystems', 'parent', 'data_composition',
                  'upload_interface', 'upload_format',
                  'mapping_security_group', 'sed', 'link', 'description', 'comments', 'tags')


class SystemRoleImportForm(NetBoxModelImportForm):
    system = DynamicModelChoiceField(
        label='Система',
        queryset=System.objects.all(),
        required=False,
        null_option='None'
    )
    subsystems = DynamicModelMultipleChoiceField(
        label='Подсистемы',
        queryset=Subsystem.objects.all()
    )

    parent = DynamicModelChoiceField(
        label='В составе роли',
        queryset=SystemRole.objects.all(),
        required=False,
        null_option='None'
    )
    slug = SlugField()

    class Meta:
        model = SystemRole
        fields = ('name', 'slug', 'system', 'subsystems', 'parent', 'data_composition',
                  'upload_interface', 'upload_format',
                  'mapping_security_group', 'sed', 'link', 'description', 'comments', 'tags')


class SystemRoleBulkEditForm(NetBoxModelBulkEditForm):
    system = DynamicModelChoiceField(
        label='Система',
        queryset=System.objects.all(),
        required=False,
        null_option='None'
    )
    subsystems = DynamicModelMultipleChoiceField(
        label='Подсистемы',
        queryset=Subsystem.objects.all()
    )

    parent = DynamicModelChoiceField(
        label='В составе роли',
        queryset=SystemRole.objects.all(),
        required=False,
        null_option='None'
    )

    model = SystemRole
    fieldsets = (
        (None, ('system', 'subsystems', 'parent',)),
    )
    nullable_fields = ('system', 'subsystems', 'parent',)


class SystemRoleFilterForm(NetBoxModelFilterSetForm):
    model = SystemRole

    name = forms.CharField(
        label='Название',
        required=False
    )

    slug = forms.CharField(
        label='короткий URL',
        required=False
    )

    system = forms.ModelMultipleChoiceField(
        label='Система',
        queryset=System.objects.all(),
        required=False
    )

    subsystems = DynamicModelMultipleChoiceField(
        label='Подсистемы',
        queryset=Subsystem.objects.all(),
        required=False
    )

    parent = forms.ModelMultipleChoiceField(
        label='Роль',
        queryset=SystemRole.objects.all(),
        required=False
    )

    tag = TagFilterField(model)


# system Role Group Form & Filter Form
class TechRoleForm(NetBoxModelForm):
    comments = CommentField()

    roles = DynamicModelMultipleChoiceField(
        label='Роли',
        queryset=SystemRole.objects.all()
    )
    slug = SlugField()

    class Meta:
        model = TechRole
        fields = ('name', 'slug', 'roles', 'comments', 'tags')


class TechRoleFilterForm(NetBoxModelFilterSetForm):
    model = TechRole

    name = forms.CharField(
        label='Название',
        required=False
    )

    slug = forms.CharField(
        label='короткий URL',
        required=False
    )

    roles = DynamicModelMultipleChoiceField(
        label='Роль',
        queryset=SystemRole.objects.all(),
        required=False
    )

    tag = TagFilterField(model)


class TechRoleImportForm(NetBoxModelImportForm):
    roles = DynamicModelMultipleChoiceField(
        label='Роли',
        queryset=SystemRole.objects.all()
    )
    slug = SlugField()

    class Meta:
        model = TechRole
        fields = ('name', 'slug', 'roles', 'description', 'tags')


class TechRoleBulkEditForm(NetBoxModelBulkEditForm):
    roles = DynamicModelMultipleChoiceField(
        label='Роли',
        queryset=SystemRole.objects.all()
    )

    model = TechRole
    fieldsets = (
        (None, ('roles',)),
    )
    nullable_fields = ('roles',)
