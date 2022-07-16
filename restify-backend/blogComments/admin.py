from django.contrib import admin

# Register your models here.
from blogComments.models import BlogComment, BlogCommentLike

admin.site.register(BlogComment)
admin.site.register(BlogCommentLike)
