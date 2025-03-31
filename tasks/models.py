from django.utils.translation import gettext as _
from django.db import models

from user.models import User
from statuses.models import Status


class Task(models.Model):
    name = models.CharField(
        max_length=255, verbose_name=_('Name'),
        unique=True, blank=False,
    )
    description = models.TextField(
        blank=True, verbose_name=_('Description'),
    )
    author = models.ForeignKey(
        User, related_name='author', verbose_name=_('Author'),
        blank=False, on_delete=models.PROTECT,
    )
    executor = models.ForeignKey(
        User, related_name='executor', verbose_name=_('Executor'),
        null=True, blank=True, default='', on_delete=models.PROTECT,
    )
    status = models.ForeignKey(
        Status, related_name='status', verbose_name=_('Status'),
        blank=False, on_delete=models.PROTECT,
    )
    created_at = models.DateTimeField(auto_now_add=True)