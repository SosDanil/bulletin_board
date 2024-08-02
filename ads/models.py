from django.db import models

from users.models import User


class Ad(models.Model):
    """Модель объявления с полями названия, цены, описания, даты создания и автора"""

    title = models.CharField(max_length=300, verbose_name='название товара')
    price = models.PositiveIntegerField(verbose_name='стоимость товара')
    description = models.TextField(verbose_name='описание', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')

    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='автор объявления', related_name='ad',
                               blank=True, null=True)

    class Meta:
        verbose_name = 'объявление'
        verbose_name_plural = 'объявления'
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.title}, цена: {self.price}'


class Review(models.Model):
    """Модель отзыва с полями текста, автора, объявления и даты создания"""

    text = models.TextField(verbose_name='содержание отзыва')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')

    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, verbose_name='объявление', related_name='review')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='автор отзыва', related_name='review',
                               blank=True, null=True)

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'

    def __str__(self):
        return f'Отзыв от {self.author} на {self.ad}: {self.text}'
