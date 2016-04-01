from django.contrib import admin

from yadel_main.models import UserAccount, Publication

# Register your models here.

class PublicationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'title_slug':('title',)}





admin.site.register(UserAccount)
admin.site.register(Publication, PublicationAdmin)
