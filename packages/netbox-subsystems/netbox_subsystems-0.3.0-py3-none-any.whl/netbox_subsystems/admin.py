from django.contrib import admin
from .models import Subsystem, System, SystemGroup, SupersetUser, EmbeddedDashboard


@admin.register(Subsystem)
class SubsystemAdmin(admin.ModelAdmin):
    list_display = ("name", 'system', 'parent', 'security_id')


@admin.register(System)
class SystemAdmin(admin.ModelAdmin):
    list_display = ("name", 'tenant',  'parent', 'security_id')


@admin.register(SystemGroup)
class SystemGroupAdmin(admin.ModelAdmin):
    list_display = ("name",)

admin.site.register(SupersetUser)
admin.site.register(EmbeddedDashboard)
