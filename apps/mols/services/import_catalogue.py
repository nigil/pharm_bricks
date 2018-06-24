from wagtail.wagtailcore.models import Page
from mols.models import MoleculesGroup, Molecule, MoleculePrices
from static_page.models import StaticPage
from rdkit.Chem import ForwardSDMolSupplier, rdMolDescriptors, Descriptors, Draw
from django.core.files.base import ContentFile
from StringIO import StringIO
import re


class CustomDrawningOptions(Draw.DrawingOptions):
    dotsPerAngstrom = 100
    useFraction = 0.8

    atomLabelFontFace = "sans"
    atomLabelFontSize = 35
    atomLabelMinFontSize = 26

    bondLineWidth = 2
    dblBondOffset = .2
    dblBondLengthFrac = .8

    defaultColor = (0, 0, 0)
    selectColor = (0, 0, 0)
    bgColor = (1, 1, 1)

    colorBonds = True
    radicalSymbol = u'\u2219'

    dash = (4, 4)

    wedgeDashedBonds = True
    showUnknownDoubleBonds = True

    # used to adjust overall scaling for molecules that have been laid out with non-standard
    # bond lengths
    coordScale = 2.0

    elemDict = {
        1: (0, 0, 0),
        7: (0, 0, 0),
        8: (0, 0, 0),
        9: (0, 0, 0),
        15: (0, 0, 0),
        16: (0, 0, 0),
        17: (0, 0, 0),
        35: (0, 0, 0),
        53: (0, 0, 0),
        0: (0, 0, 0),
    }


class RDKitClient():
    @staticmethod
    def attach_prices_to_mol(mol_page, prices):
        for quantity in prices:
            try:
                mol_price = MoleculePrices.objects.get(product=mol_page, ref=quantity)
            except MoleculePrices.DoesNotExist:
                mol_price = MoleculePrices(product=mol_page, ref=quantity)

            mol_price.price = prices[quantity]
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
                import_log.append('The element with id {} is skipped because there aro no catalogue number'.format(
                    mol_props.get('ID', '')
                ))
                continue

            try:
                catalogue_path = mol_props['Library_type']
            except KeyError:
                import_log.append('The element with id {} is skipped because there aro no catalogue path'.format(
                    mol_props.get('ID', '')
                ))
                continue

            try:
                chemical_name = mol_props['Chemical_Name']
            except KeyError:
                import_log.append('The element with id {} is skipped because there aro no chemical name'.format(
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

            default_cas_value = '000-00-0'
            cas_value = mol_props.get('CAS_number', default_cas_value)
            mol.cas = cas_value if cas_value != default_cas_value else ''

            mol_page.purity = int(mol_props.get('Purity', None))
            mol_page.slug = catalogue_number.lower().replace(' ', '-')

            if not mol_page.id:
                parent_item.add_child(instance=mol_page)
            mol_page.save()

            mol_image = Draw.MolToImage(mol, (404, 383), options=CustomDrawningOptions())
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
                              'purity: {purity}</pre>'.format(
                                    catalogue_number=catalogue_number,
                                    chemical_name=chemical_name,
                                    formula=mol_page.formula,
                                    log_p=mol_page.log_p,
                                    log_s=mol_page.log_s,
                                    mw=mol_page.mw,
                                    cas=mol_page.cas,
                                    purity=mol_page.purity))

            prices = {}
            for prop_key in mol_props:
                if prop_key.startswith('Quantity_'):
                    quantity_num = prop_key.split('_')[1]
                    try:
                        price = mol_props['Price_' + quantity_num]
                        prices[mol_props[prop_key]] = price
                    except KeyError:
                        import_log.append('Molecule {} has no price num {}'.format(catalogue_number, quantity_num))
                        continue

            if prices:
                RDKitClient.attach_prices_to_mol(mol_page, prices)

        return import_log
