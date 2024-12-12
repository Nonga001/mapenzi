from django.contrib import admin
from .models import User
from .models import Announcement


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_active')
    search_fields = ['username', 'email']
    list_filter = ['role', 'is_active']
    ordering = ['username']


# Register the Announcement model with the admin interface
@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'creator', 'created_at', 'updated_at')
    search_fields = ('title', 'content', 'creator__username')  # Search by title, content, and creator's username
    list_filter = ('created_at', 'updated_at', 'creator')  # Filter by creation and update dates, and creator
    ordering = ('-created_at',)  # Order by creation date, descending

admin.site.register(User, UserAdmin)
