from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tag, Scope


class RelationshepInlineFormser(BaseInlineFormSet):
    def clean(self):
        main_check = 0
        for form in self.forms:
            print(form.cleaned_data)
            if form.cleaned_data.get('is_main', False) == True:
                main_check += 1
        if main_check == 0:
            raise ValidationError('Укажите основной раздел')
        elif main_check > 1:
            raise ValidationError('Основным может быть только один раздел')

        return super().clean()


class ScopeInline(admin.TabularInline):
    model = Scope
    formset = RelationshepInlineFormser


@admin.register(Scope)
class Scope(admin.ModelAdmin):
    list_display = ['tag', 'article', 'is_main']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'published_at', ]
    list_filter = ['title', 'published_at']
    inlines = [ScopeInline, ]


@admin.register(Tag)
class Tag(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']

