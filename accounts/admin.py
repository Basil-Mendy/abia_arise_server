from django.contrib import admin
from .models import IndividualMember, ProGroup, GroupMember

@admin.register(IndividualMember)
class IndividualMemberAdmin(admin.ModelAdmin):
    list_display = ['abia_arise_id', 'first_name', 'last_name']
    readonly_fields = ['abia_arise_id', 'created_at', 'updated_at']

@admin.register(ProGroup)
class ProGroupAdmin(admin.ModelAdmin):
    list_display = ['group_license_number', 'name']
    readonly_fields = ['group_license_number', 'created_at', 'updated_at']

@admin.register(GroupMember)
class GroupMemberAdmin(admin.ModelAdmin):
    list_display = ['id']
    readonly_fields = ['created_at', 'updated_at']
