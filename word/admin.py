from django.contrib import admin

from word.models import Language, Word


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ['source', 'translation', 'created']
    search_fields = ['source', 'translation']
    readonly_fields = ['created', 'modified']
    ordering = ['-created', 'source']


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
