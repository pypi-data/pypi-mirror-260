from django.urls import include, path
from .models import Subsystem, System, SystemGroup
from .views import *
from netbox.views.generic import ObjectChangeLogView
from utilities.urls import get_model_urls

urlpatterns = (
    # Systems
    path('system/', SystemListView.as_view(), name='system_list'),
    path('system/add/', SystemEditView.as_view(), name='system_add'),
    path('system/import/', SystemBulkImportView.as_view(), name='system_import'),
    path('system/edit/', SystemBulkEditView.as_view(), name='system_edit'),
    path('system/delete/', SystemBulkDeleteView.as_view(), name='system_bulk_delete'),
    path('system/<int:pk>/', include(get_model_urls('netbox_subsystems', 'system'))),
    path('system/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='system_changelog', kwargs={
        'model': System
    }),

    # system-groups
    path('system-groups/', SystemGroupListView.as_view(), name='systemgroup_list'),
    path('system-groups/add/', SystemGroupEditView.as_view(), name='systemgroup_add'),
    path('system-groups/import/', SystemGroupBulkImportView.as_view(), name='systemgroup_import'),
    path('system-groups/edit/', SystemGroupBulkEditView.as_view(), name='systemgroup_edit'),
    path('system-groups/delete/', SystemGroupBulkDeleteView.as_view(), name='systemgroup_bulk_delete'),
    path('system-groups/<int:pk>/', include(get_model_urls('netbox_subsystems', 'systemgroup'))),
    path('system-groups/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='systemgroup_changelog', kwargs={
        'model': SystemGroup
    }),
    # subsystems
    path('subsystem/', SubsystemListView.as_view(), name='subsystem_list'),
    path('subsystem/add/', SubsystemEditView.as_view(), name='subsystem_add'),
    path('subsystem/import/', SubsystemBulkImportView.as_view(), name='subsystem_import'),
    path('subsystem/edit/', SubsystemBulkEditView.as_view(), name='subsystem_edit'),
    path('subsystem/delete/', SubsystemBulkDeleteView.as_view(), name='subsystem_bulk_delete'),
    path('subsystem/<int:pk>/', include(get_model_urls('netbox_subsystems', 'subsystem'))),
    path('subsystem/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='subsystem_changelog', kwargs={
        'model': Subsystem
    }),
)
