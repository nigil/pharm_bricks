import re
from StringIO import StringIO
from operator import itemgetter
from mols.models import MoleculesGroup, Molecule
from shop.models import ProductVariant
from static_page.models import StaticPage
from rdkit.Chem import ForwardSDMolSupplier, rdMolDescriptors, Descriptors, Draw, MolToSmiles
from django.core.files.base import ContentFile
from mols.services import mols_draw

try:
    import Image
except ImportError:
    from PIL import Image


class RDKitClient():
    atoms_count_to_label_size = (
        (20, 28),
        (30, 24),
        (48, 22),
        (1000, 18)
    )

    @staticmethod
    def mol_font_size(formula):
        mol_atoms_count = RDKitClient._atoms_count(formula)

        for a_count, font_size in RDKitClient.atoms_count_to_label_size:
            if mol_atoms_count < a_count:
                return font_size

    @staticmethod
    def _atoms_count(formula):
        not_alone_atoms = sum([int(i) for i in re.split(r'\D+', formula) if i])
        alone_atoms = len(re.findall(r'(\D)\D', formula))

        return not_alone_atoms + alone_atoms

    @staticmethod
    def attach_prices_to_mol(mol_page, prices):
        for quantity, price in prices:
            try:
                mol_price = ProductVariant.objects.get(product=mol_page, ref=quantity)
            except ProductVariant.DoesNotExist:
                mol_price = ProductVariant(product=mol_page, ref=quantity)

            mol_price.price = price
            mol_price.save()
            mol_page.refresh_from_db()

    @staticmethod
    def import_sdf_to_catalog(source_file):
        import_log = []
        mols = ForwardSDMolSupplier(source_file)
        mols = [mol for mol in mols if mol is not None]

        try:
            catalogue_root = MoleculesGroup.objects\
                .child_of(StaticPage.objects.get(slug='home'))\
                .get(slug='catalogue')
        except StaticPage.DoesNotExist:
            import_log.append('Please create the catalogue home page')
            return import_log

        for mol in mols:
            mol_props = mol.GetPropsAsDict()

            try:
                catalogue_number = mol_props['Catalogue_Number']
            except KeyError:
                import_log.append('The element with id {} is skipped because there are no catalogue number'.format(
                    mol_props.get('ID', '')
                ))
                continue

            try:
                catalogue_path = mol_props['Library_type']
            except KeyError:
                import_log.append('The element with id {} is skipped because there are no catalogue path'.format(
                    mol_props.get('ID', '')
                ))
                continue

            try:
                chemical_name = mol_props['Chemical_Name']
            except KeyError:
                import_log.append('The element with id {} is skipped because there are no chemical name'.format(
                    mol_props.get('ID', '')
                ))
                continue

            # catalogue structure
            catalogue_path_list = catalogue_path.split(';')
            parent_item = catalogue_root
            for item_name in catalogue_path_list:
                item_name = item_name.strip()
                item_slug = re.sub(r'[\.,;]+', '', item_name.lower().replace(' ', '-'))

                try:
                    catalogue_item = MoleculesGroup.objects.child_of(parent_item).get(slug=item_slug)
                except MoleculesGroup.DoesNotExist:
                    import_log.append('Creating molecules group {}'.format(item_name))
                    catalogue_item = MoleculesGroup(title=item_name, slug=item_slug, show_in_menus=True)
                    parent_item.add_child(instance=catalogue_item)
                    catalogue_item.save_revision().publish()

                parent_item = catalogue_item

            # molecules
            try:
                mol_page = Molecule.objects.get(catalogue_number=catalogue_number)
                import_log.append('Updating molecule {}'.format(catalogue_number))
            except Molecule.DoesNotExist:
                mol_page = Molecule(catalogue_number=catalogue_number, show_in_menus=False)
                import_log.append('Creating molecule {}'.format(catalogue_number))

            mol_page.chemical_name = mol_page.title = chemical_name
            mol_page.formula = rdMolDescriptors.CalcMolFormula(mol)
            mol_page.log_p = mol_props.get('LOGP', None)
            mol_page.log_s = mol_props.get('LOGS', None)
            mol_page.mw = round(Descriptors.MolWt(mol), 2)
            mol_page.smiles = MolToSmiles(mol)

            default_cas_value = '000-00-0'
            cas_value = mol_props.get('CAS_number', default_cas_value)
            mol.cas = cas_value if cas_value != default_cas_value else ''

            mol_page.purity = int(mol_props.get('Purity', None))
            mol_page.slug = catalogue_number.lower().replace(' ', '-')

            if not mol_page.id:
                parent_item.add_child(instance=mol_page)
            mol_page.save()

            mol_font_size = RDKitClient.mol_font_size(mol_page.formula)
            custom_drawning_options = mols_draw.CustomDrawningOptions()
            custom_drawning_options.atomLabelFontSize = mol_font_size
            custom_drawning_options.atomLabelMinFontSize = mol_font_size

            img_size = (399, 379)
            img = Image.new("RGBA", img_size, (0, 0, 0, 0))

            mol_image = mols_draw.custom_mol_to_image(
                mol,
                img_size,
                options=custom_drawning_options,
                canvas=mols_draw.CustomCanvas(img)
            )

            image_io = StringIO()
            mol_image.save(image_io, format='PNG')
            mol_page.image.save('{catalogue_number}.png'.format(catalogue_number=mol_page.slug),
                                ContentFile(image_io.getvalue()))

            mol_page.save_revision().publish()
            import_log.append('<pre>Molecule {catalogue_number} properties:\n\t'
                              'chemical_name: {chemical_name}\n\t'
                              'formula: {formula}\n\t'
                              'log_p: {log_p}\n\t'
                              'log_s: {log_s}\n\t'
                              'mw: {mw}\n\t'
                              'cas: {cas}\n\t'
                              'purity: {purity}\n\t'
                              'smiles: {smiles}</pre>'.format(
                                    catalogue_number=catalogue_number,
                                    chemical_name=chemical_name,
                                    formula=mol_page.formula,
                                    log_p=mol_page.log_p,
                                    log_s=mol_page.log_s,
                                    mw=mol_page.mw,
                                    cas=mol_page.cas,
                                    purity=mol_page.purity,
                                    smiles=mol_page.smiles))

            prices = []
            for prop_key in mol_props:
                if prop_key.startswith('Quantity_'):
                    quantity_num = prop_key.split('_')[1]
                    try:
                        price = mol_props['Price_' + quantity_num]
                        prices.append((mol_props[prop_key], price))
                        prices.sort(key=itemgetter(1))
                    except KeyError:
                        import_log.append('Molecule {} has no price num {}'.format(catalogue_number, quantity_num))
                        continue

            if prices:
                RDKitClient.attach_prices_to_mol(mol_page, prices)

        return import_log
