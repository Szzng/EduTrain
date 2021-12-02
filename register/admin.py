from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import *
from .models import MyUser

# class UserAdmin(BaseUserAdmin):
#     form = UserChangeForm
#     add_form = UserCreationForm
#
#     list_display = ('email', 'nickname', 'date_joined', 'is_admin')
#     list_filter = ('is_admin',)
#
#     # admin 페이지에서 사용자 수정할때 입력폼
#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         ('Personal info', {'fields': ('nickname', 'date_joined',)}),
#         ('Permissions', {'fields': ('is_admin',)}),
#     )
#     # admin 페이지에서 사용자 추가할때 입력폼
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'password1', 'password2', 'nickname', 'date_joined',)}
#          ),
#     )
#     search_fields = ('email', 'nickname',)
#     ordering = ('email',)
#     filter_horizontal = ()


# admin.site.register(MyUser, UserAdmin)
admin.site.register(MyUser)
admin.site.unregister(Group)