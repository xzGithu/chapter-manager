from django.contrib import admin
from chapter.models import Post
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ['title','author','status','update']
    list_filter = ['title','slug','status']
    search_fields = ['title']
admin.site.register(Post,PostAdmin)