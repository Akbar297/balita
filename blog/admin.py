from django.contrib import admin
from .models import Article, Category, Contact, Tag, Comments


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at", "updated_at")
    list_display_links = ('id', "name")


class ArticleAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created_at")
    list_display_links = ('id', "title")


admin.site.register(Category, CategoryAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Contact)
admin.site.register(Comments)
admin.site.register(Tag)
