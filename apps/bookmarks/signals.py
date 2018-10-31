import os
from django.db.models.signals import post_delete
from django.dispatch import receiver
from bookmarks.models import GeneratorResultBookmark


@receiver(post_delete, sender=GeneratorResultBookmark)
def delete_bookmark_file(sender, instance, **kwargs):
    try:
        if instance.file:
            os.remove(instance.file.path)
    except Exception:
        pass
