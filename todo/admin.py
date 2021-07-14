# -*- coding: utf-8 -*-


from django.contrib import admin
from .models import Todo

class TodoAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)
    list_display = ('id', 'title', 'important', 'user', 'datecompleted')
    list_editable = ('title', 'important', 'user', 'datecompleted')

admin.site.register(Todo, TodoAdmin)