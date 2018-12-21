from rdkit.Chem import Draw
from rdkit.Chem.Draw.cairoCanvas import Canvas, cairo, scriptPattern


class CustomCanvas(Canvas):
    def _addCanvasText1(self, text, pos, font, color=(0, 0, 0), **kwargs):
        weight = cairo.FONT_WEIGHT_BOLD
        # weight = cairo.FONT_WEIGHT_NORMAL
        self.ctx.select_font_face(font.face,
                                  cairo.FONT_SLANT_NORMAL,
                                  weight)
        text = scriptPattern.sub('', text)
        self.ctx.set_font_size(font.size)
        w, h = self.ctx.text_extents(text)[2:4]
        bw, bh = w + h * 0.4, h * 1.4
        offset = w * pos[2]
        x_position_fixer = 0
        if len(text) == 1 and text != 'O':
            x_position_fixer = int(bw / 10)
        dPos = pos[0] - w / 2. - x_position_fixer + offset, pos[1] + h / 2.
        self.ctx.set_source_rgb(*color)
        self.ctx.move_to(*dPos)
        self.ctx.show_text(text)

        return bw, bh, offset


class CustomDrawningOptions(Draw.DrawingOptions):
    dotsPerAngstrom = 100
    useFraction = 0.7

    atomLabelFontFace = "sans"
    atomLabelFontSize = 36
    atomLabelMinFontSize = 24

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
    coordScale = 3.0

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


def custom_mol_to_image(mol, size=(300, 300), kekulize=True, wedgeBonds=True, fitImage=False,
                        options=None, canvas=None, **kwargs):
    if not mol:
        raise ValueError('Null molecule provided')
    if canvas is None:
        img, canvas = Draw._createCanvas(size)
    else:
        img = canvas.image

    options = options or CustomDrawningOptions()
    if fitImage:
        options.dotsPerAngstrom = int(min(size) / 10)
    options.wedgeDashedBonds = wedgeBonds
    if 'highlightColor' in kwargs:
        color = kwargs.pop('highlightColor', (1, 0, 0))
        options.selectColor = color

    drawer = Draw.MolDrawing(canvas=canvas, drawingOptions=options)

    if kekulize:
        from rdkit import Chem
        mol = Chem.Mol(mol.ToBinary())
        Chem.Kekulize(mol)

    if not mol.GetNumConformers():
        from rdkit.Chem import AllChem
        AllChem.Compute2DCoords(mol)

    if 'legend' in kwargs:
        legend = kwargs['legend']
        del kwargs['legend']
    else:
        legend = ''

    drawer.AddMol(mol, **kwargs)

    if legend:
        from rdkit.Chem.Draw.MolDrawing import Font
        pos = size[0] / 2, int(.94 * size[1]), 0  # the 0.94 is extremely empirical
        font = Font(face='sans', size=12)
        canvas.addCanvasText(legend, pos, font)

    if kwargs.get('returnCanvas', False):
        return img, canvas, drawer
    else:
        canvas.flush()
        return img