from django.db import models
from pytils.translit import slugify
from django.conf import settings

NULLABLE = {'blank': True, "null": True}


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="наименование")
    description = models.CharField(max_length=255, verbose_name="описание")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Product(models.Model):
    objects = None
    name = models.CharField(max_length=255, verbose_name="наименование")
    description = models.TextField(blank=True, null=True, verbose_name="описание")
    image = models.ImageField(upload_to="product/image", blank=True, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                              verbose_name='Владелец', **NULLABLE)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name="категория",
        blank=True,
        null=True,
        related_name="products",
    )
    purchase_price = models.IntegerField(verbose_name="цена продажи")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="дата и время создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="дата и время последнего изменения")
    views_counter = models.PositiveIntegerField(
        default=0,
        verbose_name="количество просмотров",
        help_text="Укажите количество просмотров",
    )
    is_published = models.BooleanField(default=False, verbose_name="Опубликован")
    slug = models.SlugField(max_length=255, verbose_name="slug", null=True, blank=True)

    def unpublish(self):
        self.is_published = False
        self.save()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} {self.category}"

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["name", "category", "purchase_price"]
        permissions = [
            ('can_unpublish_product', 'Can unpublish product'),
            ('change_description_product', 'Can change product description'),
            ('change_category_product', 'Can change product category'),
        ]


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    version_number = models.CharField(max_length=100, verbose_name="номер версии")
    version_name = models.CharField(max_length=100, verbose_name="название версии")
    is_current = models.BooleanField(default=False, verbose_name="текущая версия")

    def __str__(self):
        return f"{self.version_name} ({self.version_number})"

    class Meta:
        verbose_name = "Версия"
        verbose_name_plural = "Версии"
