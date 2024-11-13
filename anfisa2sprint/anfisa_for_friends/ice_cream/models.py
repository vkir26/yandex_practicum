from django.db import models

from core.models import PublishedModel


class Category(PublishedModel):
    title = models.CharField(max_length=256, verbose_name="Название")
    slug = models.SlugField(max_length=64, unique=True, verbose_name="Слаг")
    output_order = models.PositiveSmallIntegerField(
        default=100, verbose_name="Порядок отображения"
    )

    class Meta:
        # Перевод названия моделей
        verbose_name = "категория"  # расширенное название
        verbose_name_plural = "Категории"  # расширенное название во множественном числе

    def __str__(self):
        return self.title


class Topping(PublishedModel):
    title = models.CharField(max_length=256, verbose_name="Название")
    slug = models.SlugField(max_length=64, unique=True, verbose_name="Слаг")

    class Meta:
        verbose_name = "топпинг"
        verbose_name_plural = "Топпинги"

    def __str__(self):
        return self.title


class Wrapper(PublishedModel):
    title = models.CharField(max_length=256, verbose_name="Название")

    class Meta:
        verbose_name = "обёртка"
        verbose_name_plural = "Обёртки"

    def __str__(self):
        return self.title


class IceCream(PublishedModel):
    title = models.CharField(max_length=256, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    wrapper = models.OneToOneField(
        Wrapper,
        on_delete=models.SET_NULL,
        related_name="ice_cream",
        null=True,
        blank=True,
        # Название для связанных моделей
        verbose_name="Обёртка",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="ice_creams",
        verbose_name="Категория",
    )
    toppings = models.ManyToManyField(Topping, verbose_name="Топпинги")
    is_on_main = models.BooleanField(default=False, verbose_name="На главную")

    class Meta:
        verbose_name = "мороженое"
        verbose_name_plural = "Мороженое"

    def __str__(self):
        return self.title
