from django import forms
from wagtail.admin.edit_handlers import (
    FieldPanel, FieldRowPanel, MultiFieldPanel
)
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.core import hooks

from website.blog.models import BasicPage, PostPage


@hooks.register('construct_main_menu')
def construct_main_menu(request, menu_items):
    menu_items[:] = [item for item in menu_items if item.name != 'explorer']


class BasicPageAdmin(ModelAdmin):
    model = BasicPage
    menu_icon = 'doc-empty-inverse'
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = [
        'title',
        'first_published_at',
        'latest_revision_created_at',
        'live',
    ]
    search_fields = ['title']


class PostPageAdmin(ModelAdmin):
    model = PostPage
    menu_icon = 'pick'
    menu_order = 100
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = [
        'title',
        'first_published_at',
        'latest_revision_created_at',
        'live',
    ]
    search_fields = ['title']


modeladmin_register(BasicPageAdmin)
modeladmin_register(PostPageAdmin)
