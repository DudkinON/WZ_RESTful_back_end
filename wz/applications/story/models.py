from django.db import models
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFill
from django.utils.translation import ugettext_lazy as _
from wz.applications.main.models import Languages
from wz.applications.users.models import User, Readers
from wz.helper import get_image_path


class StoryImage(models.Model):
    image = ProcessedImageField(verbose_name=_("image"),
                                upload_to=get_image_path,
                                processors=[ResizeToFill(1000, 800)],
                                format='JPEG',
                                options={'quality': 80})
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    is_active = models.BooleanField(_("is active"), default=True)
    created = models.DateTimeField(verbose_name=_("created"),
                                   auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(verbose_name=_("updated"),
                                   auto_now_add=False, auto_now=True)

    def __str__(self):
        return "user: {}, image id: {}".format(
            self.user.get_full_name, self.id)

    class Meta:
        db_table = "story_image"
        verbose_name = _('Image')
        verbose_name_plural = _('Images')

    @property
    def serialize(self):
        return {
            'image': self.image,
            'user': self.user.serialize,
            'is_active': self.is_active,
            'created': self.created,
            'updated': self.updated
        }

