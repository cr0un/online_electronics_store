from django.contrib import admin
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.forms import SetPasswordForm
from django.utils.translation import gettext_lazy as _
from users.models import User
from django.urls import reverse
from django.utils.safestring import mark_safe


class UserAdmin(DefaultUserAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'provider_link')
    search_fields = ('first_name', 'last_name', 'username')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    readonly_fields = ('last_login', 'date_joined')

    fieldsets = (
        (None, {'fields': ('username', 'password', 'provider')}),
        (_('Personal info'),
         {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'provider'),
        }),
    )

    def provider_link(self, obj):
        if obj.provider:
            link = reverse('admin:network_provider_change', args=[obj.provider.id])
            return mark_safe(f'<a href="{link}">{obj.provider}</a>')

    provider_link.short_description = 'Provider'

    # Добавляем возможность изменять пароль из Django admin
    def change_password(self, request, object_id, form_url='', extra_context=None):
        if '_changepassword' in request.POST:
            user = self.get_object(request, object_id)
            form = UserChangePasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                msg = _('Password changed successfully.')
                messages.success(request, msg)
                return HttpResponseRedirect(request.path)
            messages.error(request, _('There was an error changing the password.'))
        return self.changeform_view(request, object_id, form_url, extra_context)

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if obj:
            fieldsets = (
                (None, {'fields': ('username', 'password', 'provider')}),
                (_('Personal info'),
                 {'fields': ('first_name', 'last_name', 'email')}),
                (_('Permissions'),
                 {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
                (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
            )
        else:
            fieldsets = (
                (None, {
                    'classes': ('wide',),
                    'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'provider'),
                }),
            )
        return fieldsets

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_change_password'] = True
        return super().change_view(request, object_id, form_url, extra_context)


admin.site.register(User, UserAdmin)


class UserChangePasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password = self.fields.get('password')
        if password:
            password.help_text = password.help_text.format(**{'password_url': '../password/'})