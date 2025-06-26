from django.contrib import admin

from word.models import Word, Language


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ['source', 'translation']
    search_fields = ['source', 'translation']


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
