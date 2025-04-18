from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class DeleteViewContextMixin:
    title = _("Remove an object")
    cancel_url = None

    def get_title(self):
        return self.title

    def get_message(self):
        return _('Are you sure you want to remove') + f' "{self.object.name}"?'

    def get_cancel_url(self):
        if self.cancel_url:
            return self.cancel_url
        return reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.get_title(),
            'message': self.get_message(),
            'cancel_url': self.get_cancel_url(),
        })
        return context