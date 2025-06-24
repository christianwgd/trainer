from django.contrib import admin

from word.models import Word, Language


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ['source', 'translation']
    search_fields = ['word']


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
