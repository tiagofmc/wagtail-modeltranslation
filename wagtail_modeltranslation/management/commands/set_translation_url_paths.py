# coding: utf-8

from django.core.management.base import NoArgsCommand
from django.conf import settings

from wagtail.wagtailcore.models import Page


class Command(NoArgsCommand):
    def set_subtree(self, root, root_path, lang=None):
        setattr(root, 'url_path_'+lang, root_path)
        root.save(update_fields=['url_path_'+lang])
        for child in root.get_children():
            slug = getattr(child, 'slug_'+lang)
            if not slug or slug == '':
                slug = getattr(child, 'slug_'+settings.LANGUAGE_CODE)

            self.set_subtree(child, root_path + slug + '/', lang)

    def handle_noargs(self, **options):
        for node in Page.get_root_nodes():
            for lang in settings.LANGUAGES:
                self.set_subtree(node.specific, '/', lang=lang[0])