from mols.models import Molecule, MoleculesGroup
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os
from shutil import rmtree
from django.conf import settings


@receiver(post_delete, sender=Molecule)
def delete_molecule_image(sender, **kwargs):
    instance = kwargs.get('instance')
    try:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
    except Exception:
        pass


@receiver(post_delete, sender=MoleculesGroup)
def delete_molecule_group_images(sender, **kwargs):
    instance = kwargs.get('instance')
    for mol in instance.get_descendants():
        try:
            if os.path.isfile(mol.image.path):
                os.remove(mol.image.path)
        except Exception:
            pass

    # group_code = instance.slug
    # rmtree(os.path.join(settings.MEDIA_ROOT, group_code))

