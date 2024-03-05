from django.urls import include, path
from . import models, views
from netbox.views.generic import ObjectChangeLogView
from utilities.urls import get_model_urls

urlpatterns = (
    # SystemRole
    path('system-roles/', views.SystemRoleListView.as_view(), name='systemrole_list'),
    path('system-roles/add/', views.SystemRoleEditView.as_view(), name='systemrole_add'),
    path('system-roles/import/', views.SystemRoleBulkImportView.as_view(), name='systemrole_import'),
    path('system-roles/edit/', views.SystemRoleBulkEditView.as_view(), name='systemrole_edit'),
    path('system-roles/delete/', views.SystemRoleBulkDeleteView.as_view(), name='systemrole_bulk_delete'),
    path('system-roles/<int:pk>/', include(get_model_urls('netbox_rolesandgroups', 'systemrole'))),
    path('system-roles/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='systemrole_changelog', kwargs={
        'model': models.SystemRole
    }),

    # techrole
    path('tech-roles/', views.TechRoleListView.as_view(), name='techrole_list'),
    path('tech-roles/add/', views.TechRoleEditView.as_view(), name='techrole_add'),
    path('tech-roles/import/', views.TechRoleBulkImportView.as_view(), name='techrole_import'),
    path('tech-roles/edit/', views.TechRoleBulkEditView.as_view(), name='techrole_edit'),
    path('tech-roles/delete/', views.TechRoleBulkDeleteView.as_view(), name='techrole_bulk_delete'),
    path('tech-roles/<int:pk>/', include(get_model_urls('netbox_rolesandgroups', 'techrole'))),
    path('tech-roles/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='techrole_changelog', kwargs={
        'model': models.TechRole
    }),

)
