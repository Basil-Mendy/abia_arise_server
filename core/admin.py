from django.contrib import admin
from .models import Achievement, News, Leadership

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at']
    list_filter = ['created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['title', 'content']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Leadership)
class LeadershipAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'leadership_level', 'lga', 'ward', 'order', 'is_active', 'created_at']
    list_filter = ['leadership_level', 'is_active', 'created_at']
    search_fields = ['name', 'role', 'lga', 'ward']
    list_editable = ['order', 'is_active']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'role', 'leadership_level', 'picture', 'bio')
        }),
        ('Location Details', {
            'fields': ('lga', 'ward')
        }),
        ('Ordering & Status', {
            'fields': ('order', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
