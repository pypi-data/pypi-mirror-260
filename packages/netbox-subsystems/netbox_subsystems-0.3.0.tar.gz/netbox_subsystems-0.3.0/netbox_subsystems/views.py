from django.contrib.auth.mixins import PermissionRequiredMixin
from netbox.views import generic
from utilities.views import register_model_view
from tenancy.views import ObjectContactsView

try:
    from netbox_counterparties.views import ObjectCounterpartiesView
except:
    pass

from .models import System, SystemGroup, Subsystem, EmbeddedDashboard
from . import forms, tables, filtersets


class SystemGroupListView(generic.ObjectListView):
    queryset = SystemGroup.objects.add_related_count(
        SystemGroup.objects.all(),
        System,
        'group',
        'system_count',
        cumulative=True
    )
    filterset = filtersets.SystemGroupFilterSet
    filterset_form = forms.SystemGroupFilterForm
    table = tables.SystemGroupTable
    permission_required = "netbox_subsystems.view_system"


@register_model_view(SystemGroup)
class SystemGroupView(generic.ObjectView):
    queryset = SystemGroup.objects.all()
    permission_required = "netbox_subsystems.view_system"

    def get_extra_context(self, request, instance):
        groups = instance.get_descendants(include_self=True)
        related_models = (
            (System.objects.restrict(request.user, 'view').filter(group__in=groups), 'group_id'),
        )

        return {
            'related_models': related_models,
        }


@register_model_view(SystemGroup, 'edit')
class SystemGroupEditView(generic.ObjectEditView):
    queryset = SystemGroup.objects.all()
    form = forms.SystemGroupForm
    permission_required = "netbox_subsystems.change_system"


@register_model_view(SystemGroup, 'delete')
class SystemGroupDeleteView(generic.ObjectDeleteView):
    permission_required = "netbox_subsystems.delete_system"
    queryset = SystemGroup.objects.all()


class SystemGroupBulkImportView(generic.BulkImportView):
    queryset = SystemGroup.objects.all()
    model_form = forms.SystemGroupImportForm
    permission_required = "netbox_subsystems.view_system"


class SystemGroupBulkEditView(generic.BulkEditView):
    queryset = SystemGroup.objects.add_related_count(
        SystemGroup.objects.all(),
        System,
        'group',
        'tenant_count',
        cumulative=True
    )
    filterset = filtersets.SystemGroupFilterSet
    table = tables.SystemGroupTable
    form = forms.SystemGroupBulkEditForm
    permission_required = "netbox_subsystems.change_system"


class SystemGroupBulkDeleteView(generic.BulkDeleteView):
    permission_required = "netbox_subsystems.delete_system"
    queryset = SystemGroup.objects.add_related_count(
        SystemGroup.objects.all(),
        System,
        'group',
        'System_count',
        cumulative=True
    )
    filterset = filtersets.SystemGroupFilterSet
    table = tables.SystemGroupTable


@register_model_view(SystemGroup, 'contacts')
class SystemGroupContactsView(ObjectContactsView):
    queryset = SystemGroup.objects.all()
    permission_required = "netbox_subsystems.view_system"


class SystemListView(generic.ObjectListView):
    permission_required = "netbox_subsystems.view_system"
    queryset = System.objects.all()
    filterset = filtersets.SystemFilterSet
    filterset_form = forms.SystemFilterForm
    table = tables.SystemTable


@register_model_view(System)
class SystemView(generic.ObjectView):
    queryset = System.objects.all()
    permission_required = "netbox_subsystems.view_system"

    def get_extra_context(self, request, instance):

        ciso = EmbeddedDashboard.objects.get(name='CISO')
        filters = [{"clause": f'system = \'{instance.name}\''}]
        status_code, token = ciso.get_guest_token(filters=filters)
        parents = instance.get_descendants(include_self=True)
        related_models = (
            (System.objects.restrict(request.user, 'view').filter(parent__in=parents), 'parent_id'),
        )

        return {
            'related_models': related_models,
            'supersetDomain': ciso.user.supersetDomain,
            'EmbeddedDashboardID': ciso.EmbeddedDashboardID,
            'status_code': status_code,
            'token': token
        }


@register_model_view(System, 'edit')
class SystemEditView(generic.ObjectEditView):
    permission_required = "netbox_subsystems.change_system"
    queryset = System.objects.all()
    form = forms.SystemForm
    template_name = 'netbox_subsystems/system_edit.html'


@register_model_view(System, 'delete')
class SystemDeleteView(generic.ObjectDeleteView):
    permission_required = "netbox_subsystems.delete_system"
    queryset = System.objects.all()


class SystemBulkImportView(generic.BulkImportView):
    permission_required = "netbox_subsystems.view_system"
    queryset = System.objects.all()
    model_form = forms.SystemImportForm


class SystemBulkEditView(generic.BulkEditView):
    queryset = System.objects.all()
    filterset = filtersets.SystemFilterSet
    table = tables.SystemTable
    form = forms.SystemBulkEditForm
    permission_required = "netbox_subsystems.change_system"


class SystemBulkDeleteView(generic.BulkDeleteView):
    queryset = System.objects.all()
    filterset = filtersets.SystemFilterSet
    table = tables.SystemTable
    permission_required = "netbox_subsystems.delete_system"


@register_model_view(System, 'contacts')
class SystemContactsView(ObjectContactsView):
    queryset = System.objects.all()
    permission_required = "netbox_subsystems.view_system"


# @register_model_view(System, 'counterparties')
# class SystemCounterpartiesView(ObjectCounterpartiesView):
#     queryset = System.objects.all()


@register_model_view(Subsystem)
class SubsystemView(PermissionRequiredMixin, generic.ObjectView):
    permission_required = "netbox_subsystems.view_subsystem"
    queryset = Subsystem.objects.all()

    def get_extra_context(self, request, instance):
        parents = instance.get_descendants(include_self=True)
        related_models = (
            (Subsystem.objects.restrict(request.user, 'view').filter(parent__in=parents), 'parent_id'),
        )

        return {
            'related_models': related_models,
        }


class SubsystemListView(PermissionRequiredMixin, generic.ObjectListView):
    permission_required = "netbox_subsystems.view_subsystem"
    queryset = Subsystem.objects.all()
    table = tables.SubsystemTable
    filterset = filtersets.SubsystemFilterSet
    filterset_form = forms.SubsystemFilterForm


@register_model_view(Subsystem, 'edit')
class SubsystemEditView(PermissionRequiredMixin, generic.ObjectEditView):
    permission_required = "netbox_subsystems.change_subsystem"
    queryset = Subsystem.objects.all()
    form = forms.SubsystemForm
    template_name = 'netbox_subsystems/subsystem_edit.html'


@register_model_view(Subsystem, 'delete')
class SubsystemDeleteView(PermissionRequiredMixin, generic.ObjectDeleteView):
    permission_required = "netbox_subsystems.delete_subsystem"
    queryset = Subsystem.objects.all()


class SubsystemBulkImportView(generic.BulkImportView):
    permission_required = "netbox_subsystems.view_subsystem"
    queryset = Subsystem.objects.all()
    model_form = forms.SubsystemImportForm


class SubsystemBulkEditView(generic.BulkEditView):
    queryset = Subsystem.objects.all()
    filterset = filtersets.SubsystemFilterSet
    table = tables.SubsystemTable
    form = forms.SubsystemBulkEditForm
    permission_required = "netbox_subsystems.change_subsystem"


class SubsystemBulkDeleteView(generic.BulkDeleteView):
    queryset = Subsystem.objects.all()
    filterset = filtersets.SubsystemFilterSet
    table = tables.SubsystemTable
    permission_required = "netbox_subsystems.delete_subsystem"


@register_model_view(Subsystem, 'contacts')
class SubsystemContactsView(ObjectContactsView):
    queryset = Subsystem.objects.all()
    permission_required = "netbox_subsystems.view_subsystem"
