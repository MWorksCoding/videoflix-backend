from django.contrib import admin
from django.contrib.auth import get_user_model
from authemail.admin import EmailUserAdmin
from.models import Video
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class MyUserAdmin(EmailUserAdmin):
	fieldsets = (
		(None, {'fields': ('email', 'password')}),
		('Personal Info', {'fields': ('first_name', 'last_name')}),
		('Permissions', {'fields': ('is_active', 'is_staff', 
									   'is_superuser', 'is_verified', 
									   'groups', 'user_permissions')}),
		('Important dates', {'fields': ('last_login', 'date_joined')}),
		('Custom info', {'fields': ('date_of_birth',)}),
	)

class VideoResource(resources.ModelResource):

    class Meta:
        model = Video
 
class VideoAdmin(ImportExportModelAdmin):
    pass

@admin.register(Video)
class VideoAdmin(ImportExportModelAdmin):
    pass

admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), MyUserAdmin)