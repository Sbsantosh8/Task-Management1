from django.contrib import admin
from .models import User, Task, Project

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "email", "first_name", "last_name"]


class TaskAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "description", "assigned_to", "created_by", "status"]


class ProjectAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "total_amount"]


admin.site.register(
    Project,ProjectAdmin
)
admin.site.register(User, UserAdmin)
admin.site.register(Task, TaskAdmin)
