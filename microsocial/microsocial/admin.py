from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext as _
from microsocial.forms import CustomUserChangeForm, CustomUserCreationForm
from microsocial.models import User


class CustomUserAdmin(UserAdmin):
     form = CustomUserChangeForm
     add_form = CustomUserCreationForm
     list_display = ('email','first_name','second_name','sex',
                    'birth_date', 'locations','work',
                    'about_self', 'interests',)
     ordering = ('first_name',)
     search_fields = ('email', 'first_name', 'second_name', 'sex')
     fieldsets = (
         (None, {'fields': ('email', 'password')}),
         (_('Personal info'), {'fields': ('first_name', 'second_name',
                                          'sex', 'birth_date', 'locations','work',
                                          'about_self', 'interests',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
     )
     add_fieldsets = (
        (None, {'fields': ('email', 'password1', 'password2')}),
        (_('Personal info'), {'fields': ('first_name', 'second_name',
                                          'sex', 'birth_date', 'locations','work',
                                          'about_self', 'interests',)}),
    )

admin.site.register(User, CustomUserAdmin)