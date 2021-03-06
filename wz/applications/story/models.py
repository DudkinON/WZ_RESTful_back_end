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


class StoryTag(models.Model):
    tag = models.CharField(_("tag"), max_length=65, default=None)
    language = models.ForeignKey(Languages, verbose_name=_("language"),
                                 default=None, on_delete=models.DO_NOTHING)
    is_active = models.BooleanField(_("is active"), default=True)

    def __str__(self):
        return self.tag

    class Meta:
        db_table = "story_tag"
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')

    @property
    def serialize(self):
        return {
            'tag': self.tag,
            'language': self.language.serialize,
            'is_active': self.is_active
        }


class Story(models.Model):
    language = models.ForeignKey(Languages, verbose_name=_("language"),
                                 default=None, on_delete=models.DO_NOTHING)
    tags = models.ManyToManyField(StoryTag, verbose_name=_("tags"),
                                  default=None)
    image = models.ForeignKey(StoryImage, verbose_name=_("image"),
                              default=None, on_delete=models.DO_NOTHING)
    title = models.CharField(_("title"), max_length=255, default=None,
                             unique=True)
    description = models.TextField(_("description"), default=None)
    text = models.TextField(_("text"), default=None)
    author = models.ForeignKey(User, verbose_name=_("user"), default=None,
                               on_delete=models.DO_NOTHING)
    slug = models.CharField(_("slug"), max_length=255, default=None,
                            unique=True)
    is_active = models.BooleanField(_("is active"), default=True)
    views = models.IntegerField(default=0)

    created = models.DateTimeField(verbose_name=_("created"),
                                   auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(verbose_name=_("updated"),
                                   auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "story"
        verbose_name = _('Story')
        verbose_name_plural = _('Stories')

    def get_tags(self):
        return [tag.serialize for tag in self.tags.all()]

    @property
    def serialise(self):
        return {
            'language': self.language.serialize,
            'tags': self.get_tags(),
            'image': self.image,
            'title': self.title,
            'description': self.description,
            'text': self.text,
            'author': self.author,
            'slug': self.slug,
            'is_active': self.is_active,
            'views': self.views,
            'created': self.created,
            'updated': self.updated
        }

    @property
    def count_published_articles_by_author(self):
        """Return amount of published articles
        :return int:
        """
        return Story.objects.filter(
            author_id=self.author_id).all().count() or 0

    @property
    def count_readers(self):
        """Return amount of readers by author
        :return int:
        """
        return Readers.objects.filter(
            author_id=self.author_id).all().count() or 0
