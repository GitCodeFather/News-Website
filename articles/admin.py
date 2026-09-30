from django.contrib import admin
from django.forms import BaseInlineFormSet
from django.core.exceptions import ValidationError
from .models import Article, Tag, Scope


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        super().clean()

        main_count = 0
        for form in self.forms:
            if not form.cleaned_data or form.cleaned_data.get('DELETE'):
                continue
            if form.cleaned_data.get('is_main'):
                main_count += 1

        if main_count == 0:
            raise ValidationError('Укажите основной раздел')
        elif main_count > 1:
            raise ValidationError('Основным может быть только один раздел')


class TagInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [TagInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass



