"""Extras do faraó, em cima da base do Enoque."""
from base import *
import base as _b

def _compor_ambar(cena, t, extra=None):
    """igual ao compor da base, mas tudo que vai na camada 'cr' vira âmbar (dá para usar humano(), pt() etc. como ouro)."""
    sb, c = nova_superficie(); sr, cr = nova_superficie()
    cena(c, cr, t)
    rgb, a = para_array(sb); rr, ra = para_array(sr)
    rr = rr.max(axis=2, keepdims=True) / BR[0] * np.array(AMB, np.float32)
    out = rgb + borrar(rgb, 6) * 0.35
    out = out * (1 - ra) + rr
    if ra.max() > 0:
        out = out + borrar(rr, 12) * 1.4 + borrar(rr, 36) * 0.7
    if extra: out = extra(out, t)
    return (np.clip(out, 0, 1) * 255).astype(np.uint8)
_b.compor = _compor_ambar

def chapeu(c, Q, esc, w=LW, a=1.0):
    hx, hy = Q['cab']
    c.move_to(hx - 36 * esc, hy - 14 * esc); c.curve_to(hx - 20 * esc, hy - 20 * esc, hx + 20 * esc, hy - 20 * esc, hx + 36 * esc, hy - 14 * esc)
    traco(c, w, a=a)
    ret_arred(c, hx - 21 * esc, hy - 44 * esc, hx + 21 * esc, hy - 17 * esc, 7 * esc); pt(c, w, a=a)
    linha(c, [(hx - 21 * esc, hy - 23 * esc), (hx + 21 * esc, hy - 23 * esc)], w * 0.6, a=0.8 * a)

def chama(c, x, y, s=1.0, t=0.0, a=1.0, w=4.0, cheia=True):
    """chama em gota, ponta para cima, base em (x,y)"""
    fl = 1 + 0.08 * ruido(t, 13); inc = 6 * s * ruido(t, 9, 2)
    h = 70 * s * fl; r = 18 * s
    c.move_to(x, y); c.curve_to(x - r * 1.5, y - h * 0.25, x - r * 0.6 + inc * 0.4, y - h * 0.7, x + inc, y - h)
    c.curve_to(x + r * 0.6 + inc * 0.4, y - h * 0.7, x + r * 1.5, y - h * 0.25, x, y); c.close_path()
    if cheia:
        c.set_source_rgba(*AMB, 0.35 * a); c.fill_preserve()
    traco(c, w, AMB, a)
    elipse(c, x + inc * 0.3, y - h * 0.3, r * 0.45, h * 0.18); c.set_source_rgba(*AMB, 0.9 * a); c.fill()

def faisca(c, x, y, r, cor=BR, a=1.0, w=2.5):
    for k in range(4):
        an = k * math.pi / 2
        c.move_to(x, y); c.line_to(x + math.cos(an) * r, y + math.sin(an) * r); traco(c, w, cor, a)
    for k in range(4):
        an = math.pi / 4 + k * math.pi / 2
        c.move_to(x, y); c.line_to(x + math.cos(an) * r * 0.45, y + math.sin(an) * r * 0.45); traco(c, w * 0.7, cor, a)

def principal(cena, DUR, nome, pref):
    import sys
    if sys.argv[1] == 'teste':
        quadros(cena, [float(x) for x in sys.argv[2].split(',')], pref)
    else:
        render(cena, DUR, f'out/{nome}.mp4')
