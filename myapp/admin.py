from django.contrib import admin
from .models import Bus, User, Book

class BusAdmin(admin.ModelAdmin):
    list_display = ('id', 'bus_name', 'source', 'dest', 'nos', 'rem', 'price', 'date', 'time')
    search_fields = ('bus_name', 'source', 'dest')
    list_filter = ('date', 'time')

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

admin.site.register(Bus, BusAdmin)
admin.site.register(User)
admin.site.register(Book)


