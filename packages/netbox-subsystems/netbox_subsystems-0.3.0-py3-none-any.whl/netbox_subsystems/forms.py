from django import forms
from django.utils.translation import gettext as _
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm, NetBoxModelBulkEditForm, NetBoxModelImportForm
from utilities.forms.fields import CSVModelChoiceField
from tenancy.models import Tenant, Contact
from tenancy.forms import ContactModelFilterForm
from .models import Subsystem, System, SystemGroup, SYSTEM_FIELDS, SYSTEM_CHOICES_FIELD, SystemLevelChoices, \
    SystemPersDataLevelChoices, SystemConfLevelChoices

from django.conf import settings
from packaging import version
from utilities.forms.widgets import DatePicker

NETBOX_CURRENT_VERSION = version.parse(settings.VERSION)
if NETBOX_CURRENT_VERSION >= version.parse("3.5"):
    from utilities.forms.fields import TagFilterField, CommentField, DynamicModelChoiceField, DynamicModelMultipleChoiceField, SlugField
else:
    from utilities.forms import TagFilterField, CommentField, DynamicModelChoiceField, DynamicModelMultipleChoiceField, SlugField


class SystemGroupForm(NetBoxModelForm):
    parent = DynamicModelChoiceField(
        queryset=SystemGroup.objects.all(),
        required=False
    )
    slug = SlugField()
    fieldsets = (
        ('Группа Системы', (
            'parent', 'name', 'slug', 'description', 'tags',
        )),
    )

    class Meta:
        model = SystemGroup
        fields = [
            'parent', 'name', 'slug', 'description', 'tags',
        ]


class SystemGroupImportForm(NetBoxModelImportForm):
    parent = CSVModelChoiceField(
        queryset=SystemGroup.objects.all(),
        required=False,
        to_field_name='name',
        help_text=_('Parent group')
    )
    slug = SlugField()

    class Meta:
        model = SystemGroup
        fields = ('name', 'slug', 'parent', 'description', 'tags')


class SystemGroupBulkEditForm(NetBoxModelBulkEditForm):
    parent = DynamicModelChoiceField(
        queryset=SystemGroup.objects.all(),
        required=False
    )
    description = forms.CharField(
        label='Описание',
        max_length=200,
        required=False
    )

    model = SystemGroup
    nullable_fields = ('parent', 'description')


class SystemForm(NetBoxModelForm):
    group = DynamicModelChoiceField(label='Группа', queryset=SystemGroup.objects.all(), required=False)
    tenant = DynamicModelChoiceField(label='Учреждение', queryset=Tenant.objects.all())
    parent = DynamicModelChoiceField(queryset=System.objects.all(), required=False, null_option='NONE',
                                     label='В составе')
    comments = CommentField()
    slug = SlugField()

    class Meta:
        model = System
        fields = (
            'name', 'slug', 'group', 'parent', 'tenant', 'security_id', 'comments', 'description', 'tags'
        ) + tuple(SYSTEM_FIELDS) + tuple(SYSTEM_CHOICES_FIELD)
        widgets = {
            'comm_date': DatePicker(),
        }


class SystemImportForm(NetBoxModelImportForm):
    slug = SlugField()
    tenant = DynamicModelChoiceField(label='Учреждение', queryset=Tenant.objects.all())
    parent = DynamicModelChoiceField(queryset=System.objects.all(), required=False, null_option='NONE',
                                     label='В составе')
    group = CSVModelChoiceField(
        label='Группа',
        queryset=SystemGroup.objects.all(),
        required=False,
        to_field_name='name',
        help_text=_('Assigned group')
    )

    class Meta:
        model = System
        fields = ('name', 'slug', 'group', 'tenant', 'parent', 'description', 'comments', 'tags')


class SystemBulkEditForm(NetBoxModelBulkEditForm):
    group = DynamicModelChoiceField(
        label='Группа',
        queryset=SystemGroup.objects.all(),
        required=False
    )
    tenant = DynamicModelChoiceField(label='Учреждение', queryset=Tenant.objects.all())
    parent = DynamicModelChoiceField(queryset=System.objects.all(), required=False, null_option='NONE',
                                     label='В составе')

    model = System
    fieldsets = (
        (None, ('group', 'tenant', 'parent',)),
    )
    nullable_fields = ('group', 'tenant', 'parent',)


class SubsystemForm(NetBoxModelForm):
    system = DynamicModelChoiceField(label='Система', queryset=System.objects.all())
    parent = DynamicModelChoiceField(
        queryset=Subsystem.objects.all(),
        required=False,
        null_option='None',
        label='В составе'
    )
    comments = CommentField()
    slug = SlugField()

    class Meta:
        model = Subsystem
        fields = (
            'name', 'slug', 'parent', 'system', 'security_id', 'comments', 'description', 'tags'
        ) + tuple(SYSTEM_FIELDS) + tuple(SYSTEM_CHOICES_FIELD)
        widgets = {
            'comm_date': DatePicker(),
        }


class SubsystemImportForm(NetBoxModelImportForm):
    slug = SlugField()
    system = DynamicModelChoiceField(label='Система', queryset=System.objects.all())
    parent = DynamicModelChoiceField(
        queryset=Subsystem.objects.all(),
        required=False,
        null_option='None',
        label='В составе'
    )

    class Meta:
        model = Subsystem
        fields = ('name', 'slug', 'system', 'parent', 'description', 'comments', 'tags')


class SubsystemBulkEditForm(NetBoxModelBulkEditForm):
    system = DynamicModelChoiceField(label='Система', queryset=System.objects.all())
    parent = DynamicModelChoiceField(
        queryset=Subsystem.objects.all(),
        required=False,
        null_option='None',
        label='В составе'
    )

    model = Subsystem
    fieldsets = (
        (None, ('system', 'parent',)),
    )
    nullable_fields = ('system', 'parent',)


class SystemGroupFilterForm(NetBoxModelFilterSetForm):
    model = SystemGroup

    name = forms.CharField(
        label='Название',
        required=False
    )
    parent_id = DynamicModelChoiceField(
        queryset=SystemGroup.objects.all(),
        required=False,
        null_option='None',
        label='В составе'
    )

    tag = TagFilterField(model)


class SystemCommonFilterForm(ContactModelFilterForm, NetBoxModelFilterSetForm):
    name = forms.CharField(
        label='Название',
        required=False
    )
    security_id = forms.CharField(
        label='SSID',
        required=False
    )
    critical_level = forms.MultipleChoiceField(
        label='Уровень критичности ИС',
        choices=SystemLevelChoices,
        required=False
    )
    pers_data_category = forms.MultipleChoiceField(
        label='Уровень критичности ИС (из тенантов',
        choices=SystemPersDataLevelChoices,
        required=False
    )
    confidential_info = forms.MultipleChoiceField(
        label='Перечень конфиденциальной информации',
        choices=SystemConfLevelChoices,
        required=False
    )


class SystemFilterForm(SystemCommonFilterForm):
    model = System
    fieldsets = (
        (None, ('q', 'filter_id', 'tag', 'parent_id', 'system_group_id', 'tenant_id')),
        ('Contacts', ('contact', 'contact_tag', 'contact_role', 'contact_group'))
    )
    tag = TagFilterField(model)
    contact_tag = TagFilterField(Contact)
    parent_id = DynamicModelMultipleChoiceField(
        queryset=System.objects.all(),
        required=False,
        null_option='None',
        label='В составе'
    )
    system_group_id = DynamicModelMultipleChoiceField(
        queryset=SystemGroup.objects.all(),
        required=False,
        null_option='None',
        label='Группа'
    )
    tenant_id = DynamicModelMultipleChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        null_option='None',
        query_params={
            'group_id': '$tenant_group_id'
        },
        label='Учреждение'
    )


class SubsystemFilterForm(SystemCommonFilterForm):
    model = Subsystem
    tag = TagFilterField(model)
    parent_id = DynamicModelMultipleChoiceField(
        queryset=Subsystem.objects.all(),
        required=False,
        null_option='None',
        label='В составе'
    )
    system_id = forms.ModelMultipleChoiceField(
        label='Система',
        queryset=System.objects.all(),
        required=False
    )

