from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from PIL import Image
from wz.helper import get_image_path


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


class Pages(models.Model):
    title = models.CharField(_("title"), max_length=128, blank=True, null=True,
                             default=None)
    text = models.TextField(_("text"), blank=True, null=True, default=None)
    image = models.ImageField(_("image"), upload_to=get_image_path,
                              max_length=255, blank=True, null=True,
                              default=None)

    def __str__(self):
        title = _("Title")
        return "{}: {}".format(title, self.title)

    class Meta:
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')

