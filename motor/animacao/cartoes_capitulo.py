"""Cartões de capítulo: numeral romano grande + ícone desenhado (sem palavras, para não atrapalhar legenda/dublagem).
Troque os ícones em icone(n). Uso: python3 cartoes_capitulo.py teste | render  (saída em out/)
"""
import sys
from extras import *

DUR = 3.6
def P(pts, cx, cy, s): return [(cx + x * s, cy + y * s) for x, y in pts]

def circulo(cx, cy, r, a0=0, a1=2 * math.pi, n=40, ry=None):
    ry = r if ry is None else ry
    return [(cx + math.cos(a) * r, cy + math.sin(a) * ry) for a in np.linspace(a0, a1, n)]

def icone(n):
    L = []
    if n == 1:      # montanha
        L.append(([(-180, 120), (-40, -110), (0, -150), (40, -110), (180, 120)], False))
        L.append(([(-70, -60), (-35, -40), (0, -70), (35, -40), (70, -60)], True))
    elif n == 2:    # sol inca
        L.append((circulo(0, 0, 70), True))
        for k in range(12):
            an = k * math.pi / 6
            L.append(([(math.cos(an) * 95, math.sin(an) * 95), (math.cos(an) * 150, math.sin(an) * 150)], k % 2 == 0))
    elif n == 3:    # pena
        L.append((bez((0, 160), (-10, 40), (10, -60), (0, -170), 20), False))
        L.append((bez((0, -170), (90, -100), (70, 40), (0, 120), 20), True))
        L.append((bez((0, -170), (-90, -100), (-70, 40), (0, 120), 20), True))
    elif n == 4:    # trança
        for k in range(6):
            y = -150 + k * 50
            L.append((bez((-30, y), (30, y + 10), (30, y + 30), (-30, y + 50), 12), k % 2 == 0))
            L.append((bez((30, y), (-30, y + 10), (-30, y + 30), (30, y + 50), 12), k % 2 == 1))
        L.append(([(0, 150), (0, 180)], False))
    elif n == 5:    # floco de neve
        for k in range(6):
            an = k * math.pi / 3; ca, sa = math.cos(an), math.sin(an)
            R = lambda px, py: (px * ca - py * sa, px * sa + py * ca)
            L.append(([R(0, 0), R(150, 0)], True))
            L.append(([R(90, 0), R(120, 30)], False)); L.append(([R(90, 0), R(120, -30)], False))
    elif n == 6:    # coroa (mascapaicha) / poder
        L.append(([(-140, 60), (140, 60), (120, -20), (-120, -20), (-140, 60)], False))
        L.append(([(-40, -20), (-60, -150), (0, -100), (60, -150), (40, -20)], True))
        L.append(([(-120, 100), (120, 100)], False))
    return L

def circulo(cx, cy, r, a0=0, a1=2 * math.pi, n=40, ry=None):
    ry = r if ry is None else ry
    return [(cx + math.cos(a) * r, cy + math.sin(a) * ry) for a in np.linspace(a0, a1, n)]

NUM = {1: 'I', 2: 'II', 3: 'III', 4: 'IV', 5: 'V', 6: 'VI', 7: 'VII'}

def faz(n):
    ic = icone(n)
    # comprimento total para o desenho progressivo
    comp = [sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(p, p[1:])) for p, _ in ic]
    tot = sum(comp)
    num = texto_img(NUM[n], 190, 'SemiBold')
    def cena(c, cr, t):
        z = 1.0 + 0.04 * (t / DUR)
        for x in (c, cr): x.save(); cam(x, 960, 560, z)
        # linhas laterais
        k = eout((t - 0.15) / 0.8)
        meia = num.shape[1] / 2 + 40
        linha(c, [(960 - meia, 400), (960 - meia - 260 * k, 400)], 3, a=0.8)
        linha(c, [(960 + meia, 400), (960 + meia + 260 * k, 400)], 3, a=0.8)
        ponto(c, 960 - meia - 260 * k, 400, 5 * k); ponto(c, 960 + meia + 260 * k, 400, 5 * k)
        # ícone desenhado por partes
        prog = ease((t - 0.45) / 1.35) * tot; acc = 0
        brilho = 0.55 + 0.45 * ease((t - 1.6) / 0.5) + 0.08 * math.sin(t * 5)
        for (pts, amb), L in zip(ic, comp):
            if prog <= acc: break
            f = cl((prog - acc) / (L or 1)); acc += L
            q = parcial(P(pts, 960, 740, 1.0), f)
            if len(q) > 1:
                if amb == 'cor': corrente(c, q, elo=26, w=5)
                elif amb: linha(cr, q, 6, AMB, brilho)
                else: linha(c, q, 6)
        for x in (c, cr): x.restore()
    def extra(out, t):
        a = ease(t / 0.6); s = 1.08 - 0.08 * eout(t / 0.8)
        im = cv2.resize(num, (int(num.shape[1] * s), int(num.shape[0] * s)))
        h, w = im.shape[:2]; x0, y0 = 960 - w // 2, 400 - h // 2 - 8
        rgb, al = im[..., :3] * im[..., 3:4], im[..., 3:4] * a
        reg = out[y0:y0 + h, x0:x0 + w]
        reg[:] = reg * (1 - al) + rgb * a
        gl = np.zeros_like(out); gl[y0:y0 + h, x0:x0 + w] = rgb * a
        return out + borrar(gl, 14) * 0.6
    return cena, extra

if __name__ == '__main__':
    modo = sys.argv[1]
    for n in range(1, 7):
        cena, extra = faz(n)
        if modo == 'teste':
            quadros(cena, [3.0], f'tst/icap{n}', extra)
        else:
            render(cena, DUR, f'out/anim-inca-cap{n}.mp4', extra=extra)
