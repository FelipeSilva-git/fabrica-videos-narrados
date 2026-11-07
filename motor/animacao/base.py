"""Base das animações do Enoque: traço branco + camada âmbar com brilho, fundo preto puro
(o motor do canal põe o hachurado por trás e transforma o preto em transparente)."""
import math, subprocess, os
import numpy as np, cairo, cv2
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1920, 1080, 30
BR = (236 / 255, 232 / 255, 222 / 255)
AMB = (232 / 255, 160 / 255, 48 / 255)
LW = 5.0
FONTES = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'fontes')

def cl(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease(x): x = cl(x); return x * x * (3 - 2 * x)
def eout(x): x = cl(x); return 1 - (1 - x) ** 3
def ein(x): x = cl(x); return x ** 3
def lerp(a, b, t): return a + (b - a) * t
def lp(p, q, t): return (lerp(p[0], q[0], t), lerp(p[1], q[1], t))
def ruido(t, f=7.0, s=0): return math.sin(t * f + s) * 0.6 + math.sin(t * f * 2.3 + s * 1.7) * 0.4
def rng(seed): return np.random.RandomState(seed)

# ------------------------------------------------------------ primitivas
def traco(c, w=LW, cor=BR, a=1.0):
    c.set_source_rgba(*cor, a); c.set_line_width(w); c.stroke()

def pt(c, w=LW, cor=BR, a=1.0):
    """preenche de preto e contorna"""
    c.set_source_rgba(0, 0, 0, a); c.fill_preserve(); traco(c, w, cor, a)

def linha(c, pts, w=LW, cor=BR, a=1.0):
    c.move_to(*pts[0])
    for p in pts[1:]: c.line_to(*p)
    traco(c, w, cor, a)

def curva(c, p0, p1, p2, p3, w=LW, cor=BR, a=1.0):
    c.move_to(*p0); c.curve_to(*p1, *p2, *p3); traco(c, w, cor, a)

def elipse(c, cx, cy, rx, ry, ang=0.0):
    c.save(); c.translate(cx, cy); c.rotate(ang); c.scale(max(rx, 0.01), max(ry, 0.01))
    c.new_sub_path(); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()

def circ(c, x, y, r, w=LW, cor=BR, a=1.0, cheio=False):
    c.new_sub_path(); c.arc(x, y, r, 0, 2 * math.pi)
    if cheio: c.set_source_rgba(*cor, a); c.fill()
    else: traco(c, w, cor, a)

def ponto(c, x, y, r, cor=BR, a=1.0):
    c.new_sub_path(); c.arc(x, y, r, 0, 2 * math.pi); c.set_source_rgba(*cor, a); c.fill()

def ret_arred(c, x0, y0, x1, y1, r):
    c.new_sub_path()
    c.arc(x1 - r, y0 + r, r, -math.pi / 2, 0); c.arc(x1 - r, y1 - r, r, 0, math.pi / 2)
    c.arc(x0 + r, y1 - r, r, math.pi / 2, math.pi); c.arc(x0 + r, y0 + r, r, math.pi, 3 * math.pi / 2)
    c.close_path()

def poli(c, pts, fechar=True):
    c.move_to(*pts[0])
    for p in pts[1:]: c.line_to(*p)
    if fechar: c.close_path()

def bez(p0, p1, p2, p3, n=40):
    out = []
    for i in range(n + 1):
        t = i / n; u = 1 - t
        out.append((u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
                    u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1]))
    return out

def parcial(pts, prog):
    """corta a polilinha em 'prog' (0..1) do comprimento"""
    if prog >= 1: return pts
    if prog <= 0 or len(pts) < 2: return pts[:1]
    seg = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:])]
    alvo = sum(seg) * prog; out = [pts[0]]; acc = 0
    for (a, b), s in zip(zip(pts, pts[1:]), seg):
        if acc + s >= alvo:
            k = (alvo - acc) / (s or 1); out.append(lp(a, b, k)); return out
        out.append(b); acc += s
    return out

def osso(c, a, b, larg, w=LW, a_=1.0):
    ax, ay = a; bx, by = b
    dx, dy = bx - ax, by - ay; L = math.hypot(dx, dy) or 1
    nx, ny = -dy / L * larg, dx / L * larg
    c.move_to(ax + nx, ay + ny); c.line_to(bx + nx * 0.75, by + ny * 0.75)
    c.line_to(bx - nx * 0.75, by - ny * 0.75); c.line_to(ax - nx, ay - ny); c.close_path()
    pt(c, w, a=a_)

# ------------------------------------------------------------ pessoas (sem rosto)
POSE = dict(cab=(0, -272), pesc=(0, -240), omb_e=(-36, -228), omb_d=(36, -228),
            cot_e=(-46, -168), cot_d=(46, -168), mao_e=(-44, -108), mao_d=(44, -108),
            cint=(0, -150), barra_e=(-58, -10), barra_d=(58, -10), pe_e=(-22, 0), pe_d=(22, 0), incl=0.0)

def pose(**kw):
    p = dict(POSE); p.update(kw); return p

def mix(a, b, t):
    return {k: (lp(a[k], b[k], t) if isinstance(a[k], tuple) else lerp(a[k], b[k], t)) for k in a}

def andar(fase, base=None):
    p = dict(base or POSE); s = math.sin(fase)
    p['pe_e'] = (-22 + 22 * s, -max(0, 10 * s)); p['pe_d'] = (22 - 22 * s, -max(0, -10 * s))
    p['barra_e'] = (-58 + 8 * s, -10); p['barra_d'] = (58 + 8 * s, -10)
    p['mao_e'] = (-44 - 14 * s, -108); p['mao_d'] = (44 - 14 * s, -108)
    p['cab'] = (0, -272 - 3 * abs(math.cos(fase)))
    return p

def asa(c, ox, oy, lado, esc, abre, w, a=1.0):
    """asa de penas: lado=-1 esquerda, 1 direita. abre 0 (fechada, para baixo) .. 1 (aberta, para cima)"""
    pont = lp((lado * 70, 150), (lado * 260, -170), abre)       # ponta da asa
    meio = lp((lado * 95, -30), (lado * 190, -110), abre)
    P = lambda q: (ox + q[0] * esc, oy + q[1] * esc)
    topo = bez(P((0, 0)), P((lado * 40, -70 * abre - 10)), P(meio), P(pont), 24)
    base_ = bez(P(pont), P(lp((lado * 80, 120), (lado * 210, 10), abre)), P(lp((lado * 40, 90), (lado * 90, 60), abre)), P((lado * 8, 40)), 24)
    poli(c, topo + base_); pt(c, w, a=a)
    # penas: três fileiras de arcos ao longo da borda de baixo
    for f, fr in enumerate((0.25, 0.5, 0.75)):
        pts = [lp(topo[int(i * (len(topo) - 1) / 6)], base_[len(base_) - 1 - int(i * (len(base_) - 1) / 6)], fr) for i in range(1, 6)]
        for q0, q1 in zip(pts, pts[1:]):
            m = lp(q0, q1, 0.5); d = 10 * esc * (1 - f * 0.2)
            c.move_to(*q0); c.curve_to(m[0], m[1] + d, m[0], m[1] + d, *q1); traco(c, w * 0.55, a=0.75 * a)

def humano(c, x, y, esc=1.0, P=None, w=None, a=1.0, cabelo=None, barba=False, vestido=False, cajado=False):
    P = P or POSE
    w = w or LW * max(0.55, min(1.3, esc ** 0.5))
    Q = {k: (x + v[0] * esc, y + v[1] * esc) if isinstance(v, tuple) else v for k, v in P.items()}
    # braço de trás
    osso(c, Q['omb_e'], Q['cot_e'], 8 * esc, w, a); osso(c, Q['cot_e'], Q['mao_e'], 7 * esc, w, a)
    circ_ = lambda q, r: (elipse(c, q[0], q[1], r, r), pt(c, w, a=a))
    circ_(Q['mao_e'], 8 * esc)
    # pés
    for k in ('pe_e', 'pe_d'):
        elipse(c, Q[k][0], Q[k][1] - 4 * esc, 13 * esc, 6 * esc); pt(c, w * 0.8, a=a)
    # túnica
    ab = 1.25 if vestido else 1.0
    be = (Q['cint'][0] + (Q['barra_e'][0] - Q['cint'][0]) * ab, Q['barra_e'][1])
    bd = (Q['cint'][0] + (Q['barra_d'][0] - Q['cint'][0]) * ab, Q['barra_d'][1])
    c.move_to(*Q['omb_e']); c.line_to(*Q['omb_d'])
    c.curve_to(Q['omb_d'][0] + 6 * esc, Q['omb_d'][1] + 40 * esc, Q['cint'][0] + 30 * esc, Q['cint'][1], Q['cint'][0] + 28 * esc, Q['cint'][1] + 6 * esc)
    c.line_to(*bd)
    c.curve_to(bd[0] - 20 * esc, bd[1] + 8 * esc, be[0] + 20 * esc, be[1] + 8 * esc, *be)
    c.line_to(Q['cint'][0] - 28 * esc, Q['cint'][1] + 6 * esc)
    c.curve_to(Q['cint'][0] - 30 * esc, Q['cint'][1], Q['omb_e'][0] - 6 * esc, Q['omb_e'][1] + 40 * esc, *Q['omb_e'])
    c.close_path(); pt(c, w, a=a)
    linha(c, [(Q['cint'][0] - 27 * esc, Q['cint'][1] + 6 * esc), (Q['cint'][0] + 27 * esc, Q['cint'][1] + 6 * esc)], w * 0.7, a=0.8 * a)
    for k in (-1, 1):   # dobras
        m = lp(Q['cint'], lp(be, bd, 0.5), 0.15)
        curva(c, (m[0] + k * 12 * esc, m[1]), (m[0] + k * 16 * esc, m[1] + 50 * esc), (m[0] + k * 24 * esc, bd[1] - 60 * esc), (m[0] + k * 30 * esc, bd[1] - 6 * esc), w * 0.5, a=0.6 * a)
    # pescoço e cabeça
    hx, hy = Q['cab']
    if cabelo == 'longo':
        c.move_to(hx - 22 * esc, hy - 6 * esc); c.curve_to(hx - 34 * esc, hy + 40 * esc, hx - 30 * esc, hy + 70 * esc, hx - 18 * esc, hy + 85 * esc)
        c.line_to(hx + 18 * esc, hy + 85 * esc); c.curve_to(hx + 30 * esc, hy + 70 * esc, hx + 34 * esc, hy + 40 * esc, hx + 22 * esc, hy - 6 * esc)
        c.close_path(); pt(c, w * 0.9, a=a)
    osso(c, Q['pesc'], (hx, hy + 10 * esc), 8 * esc, w, a)
    elipse(c, hx, hy, 24 * esc, 28 * esc, P.get('incl', 0)); pt(c, w, a=a)
    if cabelo == 'longo':
        for k in (-1, 1):
            curva(c, (hx + k * 4 * esc, hy - 27 * esc), (hx + k * 22 * esc, hy - 26 * esc), (hx + k * 28 * esc, hy - 4 * esc), (hx + k * 26 * esc, hy + 10 * esc), w * 0.7, a=a)
    if barba:
        c.move_to(hx - 18 * esc, hy + 8 * esc); c.curve_to(hx - 16 * esc, hy + 40 * esc, hx - 4 * esc, hy + 54 * esc, hx, hy + 58 * esc)
        c.curve_to(hx + 4 * esc, hy + 54 * esc, hx + 16 * esc, hy + 40 * esc, hx + 18 * esc, hy + 8 * esc); pt(c, w * 0.8, a=a)
        for k in (-6, 0, 6): linha(c, [(hx + k * esc, hy + 20 * esc), (hx + k * 0.6 * esc, hy + 46 * esc)], w * 0.4, a=0.6 * a)
    # braço da frente
    osso(c, Q['omb_d'], Q['cot_d'], 8 * esc, w, a); osso(c, Q['cot_d'], Q['mao_d'], 7 * esc, w, a)
    circ_(Q['mao_d'], 8 * esc)
    if cajado:
        mx, my = Q['mao_d']
        linha(c, [(mx + 4 * esc, my - 70 * esc), (mx + 4 * esc, y)], w * 0.9, a=a)
        curva(c, (mx + 4 * esc, my - 70 * esc), (mx + 4 * esc, my - 100 * esc), (mx + 34 * esc, my - 100 * esc), (mx + 30 * esc, my - 78 * esc), w * 0.9, a=a)
    return Q

def anjo(c, x, y, esc=1.0, P=None, abre=0.5, a=1.0, w=None):
    P = P or POSE
    w = w or LW * max(0.55, min(1.3, esc ** 0.5))
    e = esc * 1.15
    ox, oy = x + P['pesc'][0] * e, y + (P['pesc'][1] + 14) * e
    for lado in (-1, 1):
        asa(c, ox + lado * 14 * e, oy, lado, e, abre, w, a)
    return humano(c, x, y, e, P, w, a)

# ------------------------------------------------------------ objetos
def livro_aberto(c, cx, cy, lw, lh, linhas=9, a=1.0, w=LW, destaque=None, cr=None, brilho=0.0):
    """livro aberto visto de frente-cima. destaque=(pagina, linha) desenha essa linha na camada âmbar"""
    # capa por baixo
    c.move_to(cx - lw - 14, cy - lh / 2 + 18); c.line_to(cx - lw - 14, cy + lh / 2 + 14)
    c.curve_to(cx - lw / 2, cy + lh / 2 + 4, cx - 20, cy + lh / 2 + 22, cx, cy + lh / 2 + 34)
    c.curve_to(cx + 20, cy + lh / 2 + 22, cx + lw / 2, cy + lh / 2 + 4, cx + lw + 14, cy + lh / 2 + 14)
    c.line_to(cx + lw + 14, cy - lh / 2 + 18); pt(c, w, a=a)
    for lado in (-1, 1):
        x0, x1 = cx, cx + lado * lw
        c.move_to(x0, cy - lh / 2 + 16)
        c.curve_to(lerp(x0, x1, 0.3), cy - lh / 2 - 18, lerp(x0, x1, 0.7), cy - lh / 2 - 6, x1, cy - lh / 2)
        c.line_to(x1, cy + lh / 2)
        c.curve_to(lerp(x0, x1, 0.7), cy + lh / 2 - 6, lerp(x0, x1, 0.3), cy + lh / 2 + 6, x0, cy + lh / 2 + 22)
        c.close_path(); pt(c, w, a=a)
        for k in range(linhas):
            yy = cy - lh / 2 + 40 + k * (lh - 70) / (linhas - 1)
            xa, xb = lerp(x0, x1, 0.12), lerp(x0, x1, 0.88 - 0.25 * ((k * 7 + (lado > 0) * 3) % 4 == 0))
            alvo = c; cor = BR; aa = 0.55 * a; ww = w * 0.6
            if destaque and destaque[0] == lado and destaque[1] == k and cr is not None:
                alvo, cor, aa, ww = cr, AMB, cl(brilho), w * 0.9
                linha(c, [(xa, yy), (xb, yy)], w * 0.6, a=0.55 * a)
            ondula = [(lerp(xa, xb, i / 12), yy + 2 * math.sin(i * 1.7 + k)) for i in range(13)]
            linha(alvo, ondula, ww, cor, aa)
    return (cx, cy)

def livro_fechado(c, cx, cy, lw, lh, esp=26, ang=0.0, a=1.0, w=LW, cruz=False, cr=None):
    c.save(); c.translate(cx, cy); c.rotate(ang)
    # lombada/espessura
    poli(c, [(-lw / 2, -lh / 2), (lw / 2, -lh / 2), (lw / 2 + esp * 0.6, -lh / 2 + esp * 0.6), (lw / 2 + esp * 0.6, lh / 2 + esp * 0.6), (-lw / 2 + esp * 0.6, lh / 2 + esp * 0.6), (-lw / 2, lh / 2)])
    pt(c, w, a=a)
    for k in range(1, 4):
        linha(c, [(lw / 2 + k * esp * 0.15, -lh / 2 + k * esp * 0.15 + 6), (lw / 2 + k * esp * 0.15, lh / 2 + k * esp * 0.15 - 2)], w * 0.4, a=0.6 * a)
    ret_arred(c, -lw / 2, -lh / 2, lw / 2, lh / 2, 6); pt(c, w, a=a)
    ret_arred(c, -lw / 2 + 14, -lh / 2 + 14, lw / 2 - 14, lh / 2 - 14, 4); traco(c, w * 0.5, a=0.7 * a)
    if cruz:
        linha(c, [(0, -lh * 0.22), (0, lh * 0.22)], w * 1.1, a=a); linha(c, [(-lw * 0.15, -lh * 0.08), (lw * 0.15, -lh * 0.08)], w * 1.1, a=a)
    c.restore()

def corrente(c, pts, elo=22, w=LW, a=1.0, cor=BR, fase=0.0):
    """elos ao longo da polilinha"""
    seg = [math.hypot(b[0] - a_[0], b[1] - a_[1]) for a_, b in zip(pts, pts[1:])]
    tot = sum(seg); n = int(tot / (elo * 0.8))
    for i in range(n):
        d = (i + 0.5) * tot / n; acc = 0
        for (p, q), s in zip(zip(pts, pts[1:]), seg):
            if acc + s >= d:
                k = (d - acc) / (s or 1); x, y = lp(p, q, k); ang = math.atan2(q[1] - p[1], q[0] - p[0]); break
            acc += s
        if i % 2 == 0:
            elipse(c, x, y, elo * 0.62, elo * 0.34, ang); c.set_source_rgba(0, 0, 0, a); c.fill_preserve(); traco(c, w * 0.75, cor, a)
        else:
            linha(c, [(x - math.cos(ang) * elo * 0.5, y - math.sin(ang) * elo * 0.5), (x + math.cos(ang) * elo * 0.5, y + math.sin(ang) * elo * 0.5)], w * 1.6, cor, a)
            linha(c, [(x - math.cos(ang) * elo * 0.5, y - math.sin(ang) * elo * 0.5), (x + math.cos(ang) * elo * 0.5, y + math.sin(ang) * elo * 0.5)], w * 0.5, (0, 0, 0), a)

def cadeado(c, x, y, s=1.0, w=LW, a=1.0, cor=BR):
    c.new_sub_path(); c.arc(x, y - 24 * s, 18 * s, math.pi, 2 * math.pi); traco(c, w, cor, a)
    linha(c, [(x - 18 * s, y - 24 * s), (x - 18 * s, y - 12 * s)], w, cor, a); linha(c, [(x + 18 * s, y - 24 * s), (x + 18 * s, y - 12 * s)], w, cor, a)
    ret_arred(c, x - 28 * s, y - 14 * s, x + 28 * s, y + 30 * s, 6 * s); c.set_source_rgba(0, 0, 0, a); c.fill_preserve(); traco(c, w, cor, a)
    circ(c, x, y + 4 * s, 5 * s, w * 0.6, cor, a); linha(c, [(x, y + 8 * s), (x, y + 18 * s)], w * 0.6, cor, a)

def casa(c, x, y, s=1.0, w=LW, a=1.0, janela=None, cr=None, luz=0.0):
    """casa antiga de teto plano. x,y = canto inferior esquerdo"""
    ww, hh = 150 * s, 110 * s
    poli(c, [(x, y), (x, y - hh), (x + ww, y - hh), (x + ww, y)]); pt(c, w, a=a)
    linha(c, [(x - 8 * s, y - hh), (x + ww + 8 * s, y - hh)], w * 1.2, a=a)
    for k in range(5): linha(c, [(x + (12 + k * 30) * s, y - hh - 2 * s), (x + (12 + k * 30) * s, y - hh + 8 * s)], w * 0.6, a=0.7 * a)
    c.move_to(x + 20 * s, y); c.line_to(x + 20 * s, y - 60 * s); c.arc(x + 40 * s, y - 60 * s, 20 * s, math.pi, 0); c.line_to(x + 60 * s, y)
    traco(c, w * 0.8, a=a)
    jx, jy = x + 95 * s, y - 75 * s
    ret_arred(c, jx, jy, jx + 32 * s, jy + 28 * s, 3 * s); traco(c, w * 0.8, a=a)
    if cr is not None and luz > 0.01:
        ret_arred(cr, jx + 4 * s, jy + 4 * s, jx + 28 * s, jy + 24 * s, 2 * s); cr.set_source_rgba(*AMB, cl(luz)); cr.fill()

def montanha(c, pts, w=LW, a=1.0, neve=True):
    poli(c, pts, fechar=False); c.line_to(pts[-1][0], 2000); c.line_to(pts[0][0], 2000); c.close_path(); pt(c, w, a=a)
    if neve:
        i = int(np.argmin([p[1] for p in pts])); px, py = pts[i]
        ls = [(px - 70, py + 70), (px - 40, py + 55), (px - 18, py + 85), (px + 10, py + 60), (px + 40, py + 90), (px + 75, py + 72)]
        linha(c, ls, w * 0.7, a=0.85 * a)

def estrela(c, x, y, r, cor=BR, a=1.0, w=2.5):
    linha(c, [(x - r, y), (x + r, y)], w, cor, a); linha(c, [(x, y - r), (x, y + r)], w, cor, a)
    ponto(c, x, y, r * 0.3, cor, a)

def nuvem(c, x, y, s=1.0, w=LW, a=1.0, n=5):
    pts = []
    for i in range(n):
        cx = x + (i - (n - 1) / 2) * 60 * s; r = (38 + 14 * math.sin(i * 2.1)) * s
        c.new_sub_path(); c.arc(cx, y - r * 0.5, r, math.pi, 2 * math.pi)
    c.set_source_rgba(0, 0, 0, a); c.fill_preserve(); traco(c, w * 0.8, a=a)
    linha(c, [(x - (n / 2) * 60 * s - 10 * s, y), (x + (n / 2) * 60 * s + 10 * s, y)], w * 0.8, a=a)

# ------------------------------------------------------------ composição
def nova_superficie():
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
    c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_join(cairo.LINE_JOIN_ROUND)
    return s, c

def para_array(sf):
    a = np.ndarray((H, W, 4), np.uint8, buffer=sf.get_data()).astype(np.float32) / 255
    return a[..., [2, 1, 0]], a[..., 3:4]

def borrar(img, sigma):
    f = 4
    p = cv2.resize(img, (W // f, H // f), interpolation=cv2.INTER_AREA)
    p = cv2.GaussianBlur(p, (0, 0), sigma / f)
    return cv2.resize(p, (W, H), interpolation=cv2.INTER_LINEAR)

def cam(c, fx, fy, z, ang=0.0):
    c.translate(W / 2, H / 2); c.scale(z, z); c.rotate(ang); c.translate(-fx, -fy)

def compor(cena, t, extra=None):
    """cena(c, cr, t) desenha em duas camadas: branca e âmbar."""
    sb, c = nova_superficie(); sr, cr = nova_superficie()
    cena(c, cr, t)
    rgb, a = para_array(sb); rr, ra = para_array(sr)
    out = rgb + borrar(rgb, 6) * 0.35
    out = out * (1 - ra) + rr
    if ra.max() > 0:
        out = out + borrar(rr, 12) * 1.4 + borrar(rr, 36) * 0.7
    if extra: out = extra(out, t)
    return (np.clip(out, 0, 1) * 255).astype(np.uint8)

def render(cena, dur, saida, t0=0.0, t1=None, extra=None):
    t1 = dur if t1 is None else t1
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                          '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '17',
                          '-pix_fmt', 'yuv420p', saida], stdin=subprocess.PIPE)
    for k in range(int(round((t1 - t0) * FPS))):
        p.stdin.write(compor(cena, t0 + k / FPS, extra).tobytes())
    p.stdin.close(); p.wait()

def quadros(cena, tempos, prefixo, extra=None):
    for t in tempos:
        cv2.imwrite(f'{prefixo}_{t:05.2f}.png', cv2.cvtColor(compor(cena, t, extra), cv2.COLOR_RGB2BGR))

def folha(arqs, saida, col=3, larg=640):
    ims = [cv2.resize(cv2.imread(a), (larg, larg * 9 // 16)) for a in arqs]
    for im, a in zip(ims, arqs):
        cv2.putText(im, os.path.basename(a), (8, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 200, 255), 1)
    while len(ims) % col: ims.append(np.zeros_like(ims[0]))
    linhas = [np.hstack(ims[i:i + col]) for i in range(0, len(ims), col)]
    cv2.imwrite(saida, np.vstack(linhas))

def texto_img(txt, tam, peso='Regular', cor=BR):
    """texto Cinzel como array RGBA float (para numerais romanos)"""
    f = ImageFont.truetype(os.path.join(FONTES, 'Cinzel[wght].ttf'), tam)
    try: f.set_variation_by_name(peso)
    except Exception: pass
    bb = f.getbbox(txt)
    im = Image.new('RGBA', (bb[2] - bb[0] + 20, bb[3] - bb[1] + 20), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((10 - bb[0], 10 - bb[1]), txt, font=f, fill=tuple(int(v * 255) for v in cor) + (255,))
    return np.asarray(im).astype(np.float32) / 255
