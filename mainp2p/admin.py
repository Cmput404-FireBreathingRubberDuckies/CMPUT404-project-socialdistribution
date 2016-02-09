from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from mainp2p.models import Post, Author

class AuthorInline(admin.StackedInline):
    model = Author
    can_delete = False
    verbose_name_plural = 'author'

class UserAdmin(BaseUserAdmin):
    inlines = (AuthorInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Post)
