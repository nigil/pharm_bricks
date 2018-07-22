import os
import glob
from django.db.models.signals import post_delete
from django.dispatch import receiver
from mols.models import Molecule, MoleculesGroup


@receiver(post_delete, sender=Molecule)
def delete_molecule_image(sender, **kwargs):
    instance = kwargs.get('instance')
    try:
        for mol_image_path in glob.glob(instance.image.path + '*'):
            os.remove(mol_image_path)
    except Exception:
        pass


@receiver(post_delete, sender=MoleculesGroup)
def delete_molecule_group_images(sender, **kwargs):
    instance = kwargs.get('instance')
    for mol in instance.get_descendants():
        try:
            for mol_image_path in glob.glob(mol.image.path + '*'):
                os.remove(mol_image_path)
        except Exception:
            pass

