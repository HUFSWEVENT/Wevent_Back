from django.contrib import admin
from .models import User, CodeForAuth

# Register your models here.
@admin.register(User)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'phoneNumber')

@admin.register(CodeForAuth)
class CodeForAuthModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'code')