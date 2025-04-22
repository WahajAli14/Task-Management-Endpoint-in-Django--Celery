from django.contrib import admin
from .models import Profile, Project, CustomUser, Task
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active')
    ordering = ('email',)
    list_per_page = 20
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'role', 'contact_number')
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

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'assignee', 'status')
    search_fields = ('title', 'project__title', 'assignee__username')
    list_filter = ('status',)
    ordering = ('project',)
    list_per_page = 20
    

admin.site.register(CustomUser, UserAdmin)    
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)