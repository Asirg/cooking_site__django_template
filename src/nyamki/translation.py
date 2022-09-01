from modeltranslation.translator import register, TranslationOptions
from nyamki.models import Category, Label, Keyword, ArticleType, Article, GroupOfIngredients, Ingredient, Unit, CookingIngredient, GroupOfInstructions, Instruction

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

@register(Label)
class LabelTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

@register(Keyword)
class KeywordTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

@register(ArticleType)
class ArticleTypeTranslationOptions(TranslationOptions):
    fields = ('name', )

@register(Article)
class ArticleTranslationOptions(TranslationOptions):
    fields = ('name', 'description', "content", 'unit_of_serverings', 'unit_of_preparation', 'unit_of_cooking', 'unit_of_passive')

@register(GroupOfIngredients)
class GroupOfIngredientsTranslationOptions(TranslationOptions):
    fields = ('name', )

@register(Ingredient)
class  IngredientTranslationOptions(TranslationOptions):
    fields = ('name', )

@register(Unit)
class  UnitTranslationOptions(TranslationOptions):
    fields = ('name', )

@register(CookingIngredient)
class  CookingIngredientTranslationOptions(TranslationOptions):
    fields = ('note', )

@register(GroupOfInstructions)
class  GroupOfInstructionsTranslationOptions(TranslationOptions):
    fields = ('name', )

@register(Instruction)
class  InstructionTranslationOptions(TranslationOptions):
    fields = ('content', )