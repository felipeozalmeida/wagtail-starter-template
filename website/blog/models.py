from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext as _
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (
    FieldPanel, InlinePanel, MultiFieldPanel, PageChooserPanel
)
from wagtail.core.fields import RichTextField
from wagtail.core.models import Orderable, Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search.index import SearchField


class BasicPage(Page):
    body = RichTextField(
        verbose_name=_('Conteúdo'),
        help_text=_('Conteúdo que será publicado.')
    )

    search_fields = Page.search_fields + [
        SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('body', classname='full'),
    ]

    parent_page_types = ['blog.IndexPage']
    subpage_types = []

    class Meta:
        verbose_name = _("página")


class PostPage(Page):
    subtitle = models.CharField(
        verbose_name=_('Subtítulo'),
        help_text=_('O subtítulo da página para os mecanismos de busca.'),
        max_length=255, blank=True
    )
    body = RichTextField(verbose_name=_('Conteúdo'))
    date = models.DateTimeField(
        verbose_name=_('Data de publicação'),
        help_text=_('Data de publicação que será exibida no site.'),
        default=now,
    )
    image = models.ForeignKey(
        'wagtailimages.Image', models.SET_NULL, '+',
        verbose_name=_('Imagem de destaque'),
        help_text=_('Imagem que servirá de capa para o post.'),
        blank=False, null=True,
    )

    search_fields = Page.search_fields + [
        SearchField('body'),
    ]

    content_panels = [
        MultiFieldPanel(Page.content_panels + [
            FieldPanel('subtitle'),
            ImageChooserPanel('image'),
        ], heading=_('Dados básicos')),
        FieldPanel('body', classname='full'),
    ]

    settings_panels = [
        FieldPanel('date'),
    ] + Page.settings_panels

    parent_page_types = ['blog.IndexPage']
    subpage_types = []

    def get_author(self):
        return self.owner.get_full_name

    # TODO: include function to return post excerpt with default length of 10

    class Meta:
        verbose_name = _("post")


class IndexPage(Page):
    content_panels = Page.content_panels + [
        InlinePanel('featured_posts', label=_('Posts em destaque'))
    ]

    subpage_types = ['blog.BasicPage', 'blog.PostPage']

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['featured_posts'] = self.get_featured_posts()
        context['posts'] = self.get_posts()
        return context

    def get_featured_posts(self):
        return [fp.post_page for fp in self.featured_posts.all()]

    def get_posts(self):
        return PostPage.objects.live().order_by('-date')

    class Meta:
        verbose_name = _("blog")

    class IndexPageFeaturedPost(Orderable):
        index_page = ParentalKey(
            'blog.IndexPage', on_delete=models.CASCADE,
            related_name='featured_posts', blank=False
        )
        post_page = models.ForeignKey(
            'blog.PostPage', on_delete=models.CASCADE,
            related_name='+', verbose_name=_('Post'), blank=False,
        )
        panels = [PageChooserPanel('post_page')]
