"""Ajudantes de desenho para animações de palitos: texto (rot/colar), setas, arcos, navio, oca, arco e flecha,
clava, fogueira, corda no pescoço. Importe com `from helpers import *` (traz também base/extras)."""
import sys
from extras import *

_cache = {}
def rot(txt, tam, cor=BR, peso='SemiBold'):
    k = (txt, tam, cor, peso)
    if k not in _cache: _cache[k] = texto_img(txt, tam, peso, cor)
    return _cache[k]

def colar(out, im, cx, cy, a=1.0, brilho=0.0):
    if a <= 0.01: return out
    h, w = im.shape[:2]; x0, y0 = int(cx - w / 2), int(cy - h / 2)
    x1, y1 = min(W, x0 + w), min(H, y0 + h); xa, ya = max(0, x0), max(0, y0)
    if x1 <= xa or y1 <= ya: return out
    sub = im[ya - y0:y1 - y0, xa - x0:x1 - x0]
    rgb, al = sub[..., :3] * sub[..., 3:4], sub[..., 3:4] * a
    reg = out[ya:y1, xa:x1]; reg[:] = reg * (1 - al) + rgb * a
    if brilho:
        gl = np.zeros_like(out); gl[ya:y1, xa:x1] = rgb * a; out += borrar(gl, 12) * brilho
    return out

def corda_pescoco(c, Q, esc, a=1.0, cor=BR, cauda=None, w=3.5):
    hx, hy = Q['pesc']
    elipse(c, hx, hy + 6 * esc, 20 * esc, 7 * esc); traco(c, w, cor, a)
    if cauda: linha(c, [(hx + 14 * esc, hy + 10 * esc)] + cauda, w, cor, a)

def seta(c, p, q, w=5, cor=BR, a=1.0, ponta=22):
    linha(c, [p, q], w, cor, a)
    an = math.atan2(q[1] - p[1], q[0] - p[0])
    for d in (2.6, -2.6):
        linha(c, [q, (q[0] + math.cos(an + d) * ponta, q[1] + math.sin(an + d) * ponta)], w, cor, a)

def arco_seta(c, cx, cy, r, a0, a1, w=6, cor=BR, a=1.0):
    pts = [(cx + math.cos(t) * r, cy + math.sin(t) * r) for t in np.linspace(a0, a1, 40)]
    linha(c, pts, w, cor, a)
    p, q = pts[-2], pts[-1]; an = math.atan2(q[1] - p[1], q[0] - p[0])
    for d in (2.5, -2.5):
        linha(c, [q, (q[0] + math.cos(an + d) * 26, q[1] + math.sin(an + d) * 26)], w, cor, a)

def navio(c, x, y, s=1.0, a=1.0, w=4.5, cor=BR):
    P = lambda px, py: (x + px * s, y + py * s)
    poli(c, [P(-120, 0), P(120, 0), P(90, 45), P(-95, 45)]); traco(c, w, cor, a)
    linha(c, [P(-5, 0), P(-5, -170)], w, cor, a); linha(c, [P(60, 0), P(60, -120)], w * 0.8, cor, a)
    c.move_to(*P(-5, -160)); c.curve_to(*P(40, -140), *P(45, -60), *P(-5, -40)); c.close_path(); traco(c, w * 0.8, cor, a)
    c.move_to(*P(60, -112)); c.curve_to(*P(92, -95), *P(95, -45), *P(60, -30)); c.close_path(); traco(c, w * 0.7, cor, a)
    linha(c, [P(-5, -170), P(10, -165), P(-5, -158)], w * 0.6, cor, a)

def onda(c, x0, x1, y, t, a=0.6, w=3):
    pts = [(x, y + 6 * math.sin(x / 40 + t * 2)) for x in np.linspace(x0, x1, 60)]
    linha(c, pts, w, a=a)

def oca(c, x, y, s=1.0, a=1.0, w=4):
    c.move_to(x - 90 * s, y); c.curve_to(x - 90 * s, y - 110 * s, x + 90 * s, y - 110 * s, x + 90 * s, y); traco(c, w, a=a)
    for k in range(1, 5):
        yy = y - k * 18 * s; dx = 90 * s * math.sqrt(max(0, 1 - (k * 18 / 82) ** 2))
        linha(c, [(x - dx, yy), (x + dx, yy)], w * 0.4, a=0.5 * a)
    linha(c, [(x - 120 * s, y), (x + 120 * s, y)], w * 0.7, a=0.7 * a)

def arco_flecha(c, x, y, s=1.0, a=1.0, cor=BR, w=4):
    c.move_to(x - 30 * s, y - 70 * s); c.curve_to(x + 30 * s, y - 40 * s, x + 30 * s, y + 40 * s, x - 30 * s, y + 70 * s); traco(c, w, cor, a)
    linha(c, [(x - 30 * s, y - 70 * s), (x - 30 * s, y + 70 * s)], w * 0.5, cor, a)
    linha(c, [(x - 60 * s, y), (x + 55 * s, y)], w * 0.8, cor, a)
    linha(c, [(x + 55 * s, y), (x + 40 * s, y - 10 * s)], w * 0.8, cor, a); linha(c, [(x + 55 * s, y), (x + 40 * s, y + 10 * s)], w * 0.8, cor, a)

def clava(c, x, y, s=1.0, a=1.0, cor=BR, w=5):
    """ibirapema: cabo longo e cabeça achatada arredondada"""
    linha(c, [(x, y + 160 * s), (x, y - 60 * s)], w * 1.4, cor, a)
    elipse(c, x, y - 105 * s, 42 * s, 55 * s); traco(c, w, cor, a)
    circ(c, x, y - 105 * s, 10 * s, w * 0.6, cor, a)
    for k in range(4):
        linha(c, [(x - 10 * s, y + (100 + k * 14) * s), (x + 10 * s, y + (106 + k * 14) * s)], w * 0.5, cor, a)
    for k in (-1, 1):
        curva(c, (x, y - 50 * s), (x + k * 30 * s, y - 30 * s), (x + k * 40 * s, y + 10 * s), (x + k * 34 * s, y + 40 * s), w * 0.5, cor, a)

def fogueira(c, x, y, s, t, a=1.0):
    for k in (-1, 0, 1):
        chama(c, x + k * 22 * s, y, s * (0.8 if k else 1.1), t + k, a)
    linha(c, [(x - 60 * s, y + 8 * s), (x + 60 * s, y - 4 * s)], 5, a=a); linha(c, [(x - 60 * s, y - 4 * s), (x + 60 * s, y + 8 * s)], 5, a=a)

