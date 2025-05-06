from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Labels(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_('Name'),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created at'),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='labels',
        verbose_name=_('Author'),
    )

    def __str__(self):
        return self.name
