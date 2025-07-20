from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,CompletedBook,ReadingChallenge

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('profile_picture',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(ReadingChallenge)
admin.site.register(CompletedBook)

