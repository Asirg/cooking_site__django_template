from django.contrib import admin
from nyamki.models import Article

from user.models import Profile, UserAvatar

class UserAvatarInline(admin.TabularInline):
    model = UserAvatar
    fields = ("image",)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display=("user",)
    readonly_fields=("save_articles",)
    
    inlines = [UserAvatarInline]