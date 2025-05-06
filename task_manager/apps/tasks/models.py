from django.db import models
from django.utils.translation import gettext as _

from task_manager.apps.labels.models import Labels
from task_manager.apps.statuses.models import Status
from task_manager.apps.user.models import User


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
        null=True, blank=True, default=None, on_delete=models.PROTECT,
    )
    status = models.ForeignKey(
        Status, related_name='status', verbose_name=_('Status'),
        blank=False, null=False, on_delete=models.PROTECT,
    )
    labels = models.ManyToManyField(
        Labels, blank=True, related_name='tasks', verbose_name=_('Labels'),
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
