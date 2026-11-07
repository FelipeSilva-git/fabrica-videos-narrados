"""Transforma fotos reais em "documentos" prontos para o motor (comando `documento:` do storyboard).

Cada foto vira um PNG 1920x1080 com fundo transparente: a foto com borda de papel, levemente girada,
com sombra, e um selo no canto ("REGISTRO REAL" + autor + licença), que já cumpre o crédito das licenças CC BY.

Uso:
  python3 documento.py <pasta_com_fotos> <CREDITOS.md> <pasta_de_saida> [--selo "REGISTRO REAL"] [--sepia] [--cor 255,180,64]

- As fotos devem começar com um código (ex.: r01-...jpg). O CREDITOS.md é o que o commons.py gera.
- --sepia: para gravuras e páginas de livro antigo.
"""
import re, os, glob, argparse
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageEnhance

FONTES = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'fontes')
a = argparse.ArgumentParser()
a.add_argument('fotos'); a.add_argument('creditos'); a.add_argument('saida')
a.add_argument('--selo', default='REGISTRO REAL')
a.add_argument('--sepia', action='store_true')
a.add_argument('--cor', default='255,180,64', help='cor do selo R,G,B')
o = a.parse_args()
COR = tuple(int(x) for x in o.cor.split(','))
fa = ImageFont.truetype(os.path.join(FONTES, 'Anton-Regular.ttf'), 34)
fc = ImageFont.truetype(os.path.join(FONTES, 'CormorantGaramond-Italic[wght].ttf'), 28)

cred = {}
for l in open(o.creditos, encoding='utf-8'):
    m = re.match(r'\| `([a-z]?\d+)[^`]*` \| (.*?) \| (.*?) \| (.*?) \|', l)
    if m:
        autor = re.sub(r'\s+', ' ', m.group(4)).strip()
        autor = re.split(r'[\n;,(]| from | at ', autor)[0].strip()[:38] or 'Wikimedia Commons'
        cred[m.group(1)] = (autor, m.group(3).strip())

os.makedirs(o.saida, exist_ok=True)
n = 0
for f in sorted(glob.glob(os.path.join(o.fotos, '*.*'))):
    if not f.lower().endswith(('.jpg', '.jpeg', '.png')) or os.path.getsize(f) == 0:
        continue
    k = os.path.basename(f).split('-')[0]
    im = Image.open(f).convert('RGB')
    if o.sepia:
        im = ImageOps.colorize(ImageOps.autocontrast(im.convert('L'), cutoff=1), (25, 18, 10), (225, 205, 165))
    else:
        im = ImageEnhance.Contrast(ImageEnhance.Color(im).enhance(0.85)).enhance(1.05)
    hh = 840; ww = int(im.width * hh / im.height)
    if ww > 1500: ww = 1500; hh = int(im.height * ww / im.width)
    im = im.resize((ww, hh), Image.LANCZOS)
    im = ImageOps.expand(im, border=16, fill=(236, 230, 218)).convert('RGBA')
    cr = im.rotate(-1.1 if n % 2 else 0.9, expand=True, resample=Image.BICUBIC); n += 1
    can = Image.new('RGBA', (1920, 1080), (0, 0, 0, 0))
    px = (1920 - cr.width) // 2; py = (1080 - cr.height) // 2 - 30
    sh = Image.new('L', (1920, 1080), 0)
    ImageDraw.Draw(sh).rectangle([px + 10, py + 16, px + cr.width + 10, py + cr.height + 16], fill=210)
    sombra = Image.new('RGBA', (1920, 1080), (0, 0, 0, 0)); sombra.putalpha(sh.filter(ImageFilter.GaussianBlur(24)))
    can = Image.alpha_composite(can, sombra); can.alpha_composite(cr, (px, py))
    autor, lic = cred.get(k, ('', ''))
    linha = f'Foto: {autor} · {lic}' if autor else 'Domínio público'
    d = ImageDraw.Draw(can); x, y = 70, 962
    w = max(380, int(d.textlength(linha, font=fc)) + 40)
    d.rectangle([x - 18, y - 14, x + w, y + 92], fill=(0, 0, 0, 175), outline=COR + (255,), width=3)
    d.text((x, y - 6), o.selo, font=fa, fill=COR + (255,))
    d.text((x, y + 44), linha, font=fc, fill=(235, 235, 235, 255))
    can.save(os.path.join(o.saida, f'doc-{k}.png'))
    print('ok', k, linha)
