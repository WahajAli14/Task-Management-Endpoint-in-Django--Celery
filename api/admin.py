from django.contrib import admin
from .models import Profile, Project, Task, Document, Comment
# Register your models here.



class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'contact_number')
    search_fields = ('user__username', 'role')
    list_filter = ('role',)
    ordering = ('user',)
    list_per_page = 20

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'manager', 'start_date', 'end_date')
    search_fields = ('title', 'manager__username')
    list_filter = ('start_date',)
    ordering = ('start_date',)
    list_per_page = 20
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Project, ProjectAdmin)