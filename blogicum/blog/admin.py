from django.contrib import admin

from blog.models import Category, Comment, Location, Post


admin.site.register(Category)
admin.site.register(Location)
admin.site.register(Comment)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'pub_date', 'category')
    list_filter = ('pub_date', 'category')
    date_hierarchy = 'pub_date'
    search_fields = ('title', 'description')
