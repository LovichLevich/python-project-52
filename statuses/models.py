from django.db import models
from django.utils.translation import gettext_lazy as _

class Status(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_("Имя")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Дата создания")
    )

    class Meta:
        verbose_name = _("Статус")
        verbose_name_plural = _("Статусы")
        ordering = ["id"]  # Сортировка по ID, чтобы записи шли в порядке создания

    def __str__(self):
        return self.name
