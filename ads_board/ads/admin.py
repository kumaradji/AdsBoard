from django.contrib import admin
from accounts.models import CustomUser
from ads.models import Response, Advert


class PostCategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Advert._meta.get_fields()]
    list_filter = ('post', 'category')
    search_fields = ('post', 'category__name')


admin.site.register(CustomUser),
admin.site.register(Advert),
admin.site.register(Response),
