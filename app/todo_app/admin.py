from django.contrib import admin

from todo_app.models import ToDo


class ToDoAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'state',
        'due_date',
    )
    search_fields = (
        'user__first_name',
        'user__last_name',
        'user__email',
    )

    # objects should not be writable!
    readonly_fields = (
        'user',
        'title',
        'description',
        'state',
        'due_date',
    )


admin.site.register(ToDo, ToDoAdmin)
