from import_export.admin import ImportExportModelAdmin
from import_export import fields, resources
from django.contrib import admin
from import_export.widgets import ForeignKeyWidget

from accounts.models import *


class UserResources(resources.ModelResource):
    user = fields.Field(
        column_name='user',
        attribute='user',
        widget=ForeignKeyWidget(User, 'username')
    )

    class Meta:
        model = UserProfile


class UserProfileAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['user', 'creator', 'location', 'mobile_number']
    resource_class = UserResources
    search_fields = ['mobile_number', 'user__username', 'location']
    list_filter = ['gender', 'creator']

class InstagramResource(resources.ModelResource):

    class Meta:
        model = InstagramData


class InstagramDataAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = InstagramResource
    search_fields =  ['username']



class ContactAdmin(admin.ModelAdmin):
    list_display = ['mobile_number', 'user_profile', 'city']
    search_fields = ['mobile_number', 'user_profile__user__username']




admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(SocialMedia)
admin.site.register(InstagramData, InstagramDataAdmin)
admin.site.register(TwitterData)
admin.site.register(FacebookData)
admin.site.register(YoutubeData)
admin.site.register(YoutubeAuth)
admin.site.register(BankDetail)
admin.site.register(Instagram_temp_data)
