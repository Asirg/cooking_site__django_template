from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

class Category(models.Model):
    name = models.CharField(verbose_name="Название", max_length=50)
    for_article = models.BooleanField(verbose_name="Для статей")
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    image = models.ImageField("Изображение", upload_to="category_image/", blank=True, null=True)
    url = models.SlugField(null=True)

    def __str__(self) -> str:
        return self.name

    class Meta():
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class Label(models.Model):
    name = models.CharField(verbose_name="Название", max_length=50)
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField("Изображение", upload_to="label_image/", blank=True, null=True)
    url = models.SlugField(null=True)

    def __str__(self) -> str:
        return self.name

    class Meta():
        verbose_name = "Метка"
        verbose_name_plural = "Метки"

class Keyword(models.Model):
    name = models.CharField(verbose_name="Название", max_length=50)
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    image = models.ImageField("Изображение", upload_to="keyword_image/", blank=True, null=True)
    url = models.SlugField(null=True)

    def __str__(self) -> str:
        return self.name

    class Meta():
        verbose_name = "Ключевое слово"
        verbose_name_plural = "Ключевые слова"

class ArticleType(models.Model):
    name = models.CharField(verbose_name="Название", max_length=50)

    def __str__(self) -> str:
        return self.name

    class Meta():
        verbose_name = "Тип статьи"
        verbose_name_plural = "Типы статей"


class Article(models.Model):
    author = models.ForeignKey(
        to = get_user_model(), on_delete=models.SET_NULL, null=True, verbose_name="Автор"
    )
    date = models.DateTimeField("Дата создания", auto_now_add=True)
    update_date = models.DateTimeField("Дата обновления", auto_now=True)


    name = models.CharField("Название", max_length=100)
    url = models.SlugField()
    image = models.ImageField("Изображение", upload_to="article/")
    description = models.TextField("Описание")
    content = models.TextField("Контент",  blank=True, null=True)

    draft = models.BooleanField("Черновик")
    type = models.ForeignKey(
        to=ArticleType, on_delete=models.SET_NULL, null=True, verbose_name="Тип статьи"
    )


    number_of_serverings = models.SmallIntegerField("Количество порций", blank=True, null=True)
    unit_of_serverings = models.CharField("Единица измерения порции", max_length=20, blank=True, null=True)

    preparation_time = models.FloatField("Время подготовки", blank=True, null=True)
    unit_of_preparation = models.CharField("Единица измерения подготовки", max_length=20, blank=True, null=True)

    cooking_time = models.FloatField("Время приготовления", blank=True, null=True)
    unit_of_cooking = models.CharField("Единица измерения приготовления", max_length=20, blank=True, null=True)

    passive_time = models.FloatField("Пассивное время", blank=True, null=True)
    unit_of_passive = models.CharField("Единица измерения пассивного времени", max_length=20, blank=True, null=True)

    categories = models.ManyToManyField(
        to=Category, blank=True, verbose_name="Категории", related_name="article_categories"
    )

    labels = models.ManyToManyField(
        to=Label, blank=True, verbose_name="Метки", related_name="article_labels"
    )

    keywords = models.ManyToManyField(
        to=Keyword, blank=True, verbose_name="Ключевые слова", related_name="article_keywords"
    )

    def get_nutritional_value(self) -> dict:
        nutritional_value = {
            "calories": 0,
            "proteins": 0,
            "carbohydrates": 0,
            "fats": 0,
        }
        for group in self.groupofingredients_set.all():
            for ingredient in group.cookingingredient_set.all():
                weight = ingredient.value * ingredient.unit.in_grams
                nutritional_value['calories'] +=  ingredient.ingredient.calories * weight / 100
                nutritional_value['proteins'] +=  ingredient.ingredient.proteins  * weight / 100
                nutritional_value['carbohydrates'] +=  ingredient.ingredient.carbohydrates * weight / 100
                nutritional_value['fats'] +=  ingredient.ingredient.fats * weight / 100
        return nutritional_value

    def __str__(self) -> str:
        return self.name

    class Meta():
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"

class GroupOfIngredients(models.Model):
    name = models.CharField("Название", max_length=100)
    article = models.ForeignKey(
        to=Article, on_delete=models.CASCADE, verbose_name = "Рецепт"
    )
    

    def __str__(self) -> str:
        return self.name

    class Meta():
        verbose_name = "Группа ингредиентов"
        verbose_name_plural = "Группы ингредиентов"

class Ingredient(models.Model):
    name = models.CharField("Название", max_length=50)
    calories = models.FloatField("Калории")
    proteins = models.FloatField("Белки")
    carbohydrates = models.FloatField("Углеводы")
    fats = models.FloatField("Жиры")

    def __str__(self) -> str:
        return self.name

    class Meta():
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

class Unit(models.Model):
    name = models.CharField("Название", max_length=50)
    in_grams = models.SmallIntegerField("Количество в граммах")

    def __str__(self) -> str:
        return self.name

    class Meta():
        verbose_name = "Единица измерения"
        verbose_name_plural = "Единицы измерения"

class CookingIngredient(models.Model):
    group_of_ingredients = models.ForeignKey(
        to=GroupOfIngredients, on_delete=models.CASCADE, verbose_name="Группа ингредиентов"
    )
    ingredient = models.ForeignKey(
        to=Ingredient, on_delete=models.CASCADE, verbose_name="Ингредиент"
    )
    unit = models.ForeignKey(
        to=Unit, on_delete=models.CASCADE, verbose_name="Единица измерения"
    )
    value = models.FloatField("Количество")
    note = models.CharField("Примечание", max_length=100, null=True, blank=True)

    def __str__(self) -> str:
        return self.ingredient.name

    def calc_nutritional_value():
        values = {
            "calories":0,
            "proteins":0,
            "carbohydrates":0,
            "fats":0,
        }

    class Meta():
        verbose_name = "Ингредиент в рецепте"
        verbose_name_plural = "Ингредиенты в рецепте"
    

class GroupOfInstructions(models.Model):
    name = models.CharField("Название", max_length=100)
    article = models.ForeignKey(
        to=Article, on_delete=models.CASCADE, verbose_name = "Рецепт"
    )

    def __str__(self) -> str:
        return self.name

    class Meta():
        verbose_name = "Группа инструкций"
        verbose_name_plural = "Группы инструкций"

class Instruction(models.Model):
    group_of_instructions = models.ForeignKey(
        to=GroupOfInstructions, on_delete=models.CASCADE, verbose_name="Группа инструкций"
    )
    content = models.TextField("контент")
    image = models.ImageField("Изображение", upload_to="instruction/")

    def __str__(self) -> str:
        return self.group_of_instructions.name

    class Meta():
        verbose_name = "Инструкция"
        verbose_name_plural = "Инструкции"

class Comment(models.Model):
    user = models.ForeignKey(
        to = get_user_model(), on_delete=models.CASCADE
    )
    article = models.ForeignKey(
        to = Article, on_delete=models.CASCADE
    )
    parent = models.ForeignKey(
        to = 'self', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Отцовский комментарий", 
    )
    content = models.TextField("Содержание")
    date = models.DateTimeField("Дата", auto_now_add=True)

    class Meta():
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
