from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Languages(models.Model):
    code = models.CharField(max_length=4, primary_key=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        lang = _("Language")
        return "{}: {}".format(lang, self.code)

    class Meta:
        verbose_name = _('Language')
        verbose_name_plural = _('Languages')

    @property
    def serialize(self):
        return {
            'code': self.code,
            'is_active': self.is_active
        }

