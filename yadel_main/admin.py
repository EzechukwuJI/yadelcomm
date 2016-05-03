from django.contrib import admin

from yadel_main.models import *

# Register your models here.

class PublicationAdmin(admin.ModelAdmin):
	list_display=('title','posted_by','press_material','media','date_posted','status','redirect_url',)
	list_filter = ('status','press_material',)
	prepopulated_fields = {'title_slug':('title',)}





admin.site.register(UserAccount)
admin.site.register(Publication, PublicationAdmin)
admin.site.register(MediaCategory)
admin.site.register(MediaNames)
admin.site.register(MediaContact)

