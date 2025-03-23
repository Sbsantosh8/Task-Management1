from django.contrib import admin
from .models import User, Task

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "email", "first_name", "last_name"]


class TaskAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "description", "assigned_to"]


admin.site.register(User, UserAdmin)
admin.site.register(Task, TaskAdmin)
