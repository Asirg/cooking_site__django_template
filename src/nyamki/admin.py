from django.utils.safestring import mark_safe
from django.contrib import admin
from django import forms

from ckeditor_uploader.widgets import CKEditorUploadingWidget
from modeltranslation.admin import TranslationAdmin

from nyamki.models import ArticleType, Category, Label, Keyword, Article, GroupOfIngredients, Ingredient, Unit, CookingIngredient, GroupOfInstructions, Instruction, ArticleType, Comment

# Register your models here.

class ShowImage():
    def ShowImage(self, obj):
        return mark_safe(f"<img src={obj.image.url} height='400px'>")

    ShowImage.short_description = "Изображение"

@admin.register(Category)
class CategoryAdmin(ShowImage, TranslationAdmin):
    list_display = ("name_ru", "id")

    readonly_fields = ("ShowImage", )
    fieldsets = (
        ("Основное", {
            "fields": (
                        ("name_ru", "name_uk", "for_article" ),
                        ("description_ru", "description_uk"),
                    )
        }),

        ("Дополнительное", {
            "fields": ("ShowImage", "image", "url", )
        }),
    )

    prepopulated_fields = {"url": ('name',)}

@admin.register(Label)
class LabelAdmin(ShowImage, TranslationAdmin):
    list_display = ("name_ru", )

    readonly_fields = ("ShowImage", )
    fieldsets = (
        ("Основное", {
            "fields": (
                        ("name_ru", "name_uk", ),
                        ("description_ru", "description_uk"),
                    )
        }),

        ("Дополнительное", {
            "fields": ("ShowImage", "image", "url", )
        }),
    )

    prepopulated_fields = {"url": ('name',)}

@admin.register(Keyword)
class KeywordAdmin(ShowImage, TranslationAdmin):
    list_display = ("name_ru", )

    readonly_fields = ("ShowImage", )
    fieldsets = (
        ("Основное", {
            "fields": (
                        ("name_ru", "name_uk", ),
                        ("description_ru", "description_uk"),
                    )
        }),

        ("Дополнительное", {
            "fields": ("ShowImage", "image", "url", )
        }),
    )

    prepopulated_fields = {"url": ('name',)}

class GroupOfInstructionsInline(admin.TabularInline):
    model = GroupOfInstructions
    fields = ("name_ru", "name_uk", "get_link")
    readonly_fields = ("get_link", )
    extra = 1

    def get_link(self, obj):
        return mark_safe(f"<a href='/admin/nyamki/groupofinstructions/{obj.pk}' target='_blank'>{obj.name}</a>")

class GroupOfIngredientsInline(admin.TabularInline):
    model = GroupOfIngredients
    fields = ("name_ru", "name_uk", "get_link",)
    readonly_fields = ("get_link", )
    extra = 1

    def get_link(self, obj):
        return mark_safe(f"<a href='/admin/nyamki/groupofingredients/{obj.pk}' target='_blank'>{obj.name}</a>")

class ArticleAdminForm(forms.ModelForm):
    content_ru = forms.CharField(
        label = "Дополнительной описание [ru]", 
        widget=CKEditorUploadingWidget(),
        required=False)

    content_uk = forms.CharField(
        label = "Дополнительной описание [uk]", 
        widget=CKEditorUploadingWidget(),
        required=False)

    class Meta():
        model = Article
        fields = "__all__"

@admin.register(Article)
class ArticleAdmin(TranslationAdmin):
    list_display = ("name_ru", "type", "show_categories", "show_keyword", "author", "date", "draft")
    list_editable = ("author", "type", "draft")
    readonly_fields = ("date", "update_date")

    list_filter = ("draft", "type", "author")
    search_fields = ("name", )

    form = ArticleAdminForm

    # readonly_fields = 
    fieldsets = (
        ("Основное", {
          "fields": (("name_ru", "name_uk", "url", ),
                     ("author", "type", "draft", ),
                     ("categories", "labels", "keywords"),
                     ( "date", "update_date"),
                     ("description_ru", "description_uk"),
                     ("content_ru", "content_uk"),
                     ("image", ))
        }),
        ("Приготовление", {
          "fields": (("number_of_serverings", "unit_of_serverings_ru", "unit_of_serverings_uk"),
                    ("preparation_time", "unit_of_preparation_ru", "unit_of_preparation_uk"),
                    ("cooking_time", "unit_of_cooking_ru", "unit_of_cooking_uk"),
                    ("passive_time", "unit_of_passive_ru", "unit_of_passive_uk"))
        }),
    )

    inlines = (GroupOfIngredientsInline, GroupOfInstructionsInline, )
    actions = ("publish", "unpublish")

    prepopulated_fields = {"url": ('name',)}

    def show_categories(self, obj):
        return ", ".join([x[0] for x in obj.categories.values_list('name')])
    
    def show_keyword(self, obj):
        return ", ".join([x[0] for x in obj.keywords.values_list('name')])

    def publish(self, request, queryset):
        row_update = queryset.update(draft=False)
        self.message_user(request, "Записи обновленны")

    def unpublish(self, request, queryset):
        row_update = queryset.update(draft=True)
        self.message_user(request, "Записи обновленны")
    
    def get_form(self, request, obj=None, **kwargs):
        kwargs['widgets'] = {
            'unit_of_serverings': forms.TextInput(attrs={'placeholder': 'шт., кг., '}),
            'unit_of_preparation': forms.TextInput(attrs={'placeholder': 'м., ч., '}),
            'unit_of_cooking': forms.TextInput(attrs={'placeholder': 'м., ч., '}),
            'unit_of_passive': forms.TextInput(attrs={'placeholder': 'м., ч., '}),
        }
        return super().get_form(request, obj, **kwargs)

class CookingIngredientInline(admin.TabularInline):
    model = CookingIngredient
    extra = 1

    fields = ("ingredient", "unit", "value", "note_ru", "note_uk")

    
@admin.register(GroupOfIngredients)
class GroupOfIngredientsAdmin(admin.ModelAdmin):
    list_display = ("name_ru", "article")
    list_display_links = ("name_ru", )
    
    fieldsets = (
        ("", { "fields":(
                        ("name_ru", "name_uk"),
                        ),

        },),
    )

    inlines = [CookingIngredientInline, ]
class InstructionInline(admin.TabularInline):
    model = Instruction
    extra = 1

    fields = ("content_ru", "content_uk", 'image')

@admin.register(GroupOfInstructions)
class GroupOfIngredientsAdmin(TranslationAdmin):
    list_display = ("name_ru", "article")
    list_display_links = ("name_ru", )
    
    fieldsets = (
        ("", { "fields":(
                        ("name_ru", "name_uk"),
                        ),

        },),
    )

    inlines = [InstructionInline, ]
    
@admin.register(ArticleType)
class ArticleTypeAdmin(admin.ModelAdmin):
    list_display = ("name_ru",)
    list_display_links = ("name_ru", )

    fieldsets = (
        ("", { "fields":(
                        ("name_ru", "name_uk"),
                        ),

        },),
    )

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name_ru",)
    list_display_links = ("name_ru", )

    fieldsets = (
        ("", { "fields":(
                        ("name_ru", "name_uk"),
                        ('calories', ),
                        ('proteins', ),
                        ('carbohydrates', ),
                        ('fats', ),
                        ),

        },),
    )

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ("name_ru",)
    list_display_links = ("name_ru", )

    fieldsets = (
        ("", { "fields":(
                        ("name_ru", "name_uk"),
                        ('in_grams', ),
                        ),

        },),
    )

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "article", "date")