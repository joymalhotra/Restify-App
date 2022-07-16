from django.contrib import admin

# Register your models here.
from blogs.models import Blog, BlogLike

admin.site.register(Blog)
admin.site.register(BlogLike)
