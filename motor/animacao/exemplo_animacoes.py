"""EXEMPLO REAL (episódio "a menina que dormiu por 500 anos"). Copie e troque as cenas.
Cada animação = (função de cena, duração em s, nome do arquivo, função extra para textos).
Uso:
python3 anims_inca.py teste <nome> 1.0,2.5 | python3 anims_inca.py render <nome|todos>"""
import sys
from helpers import *   # rot, colar, seta, arco_seta, corda_pescoco… (e base/extras)

def montanha(c, x, y, w, h, a=1.0, cor=BR, neve=True, wl=4):
    linha(c, [(x - w / 2, y), (x - w * 0.12, y - h * 0.86), (x, y - h), (x + w * 0.1, y - h * 0.9), (x + w / 2, y)], wl, cor, a)
    if neve:
        linha(c, [(x - w * 0.16, y - h * 0.78), (x - w * 0.07, y - h * 0.72), (x, y - h * 0.8), (x + w * 0.06, y - h * 0.73), (x + w * 0.13, y - h * 0.8)], wl * 0.6, cor, 0.7 * a)

def andes(c, t, a=1.0):
    """mapa estilizado: a cordilheira descendo de norte a sul, e o litoral"""
    costa = [(520, 80), (600, 230), (690, 420), (760, 560), (800, 700), (840, 860), (880, 1040)]
    linha(c, costa, 3, a=0.45 * a)
    for i, (x, y) in enumerate([(700, 160), (760, 290), (820, 420), (880, 540), (930, 650), (960, 770), (990, 880), (1010, 990)]):
        montanha(c, x + 40, y + 40, 90, 70, 0.75 * a, neve=False, wl=3)
CUSCO = (900, 470); LLULLA = (1040, 860)
def estrela(c, x, y, r, cor=AMB, a=1.0, w=4):
    pts = []
    for k in range(10):
        rr = r if k % 2 == 0 else r * 0.45; an = -math.pi / 2 + k * math.pi / 5
        pts.append((x + math.cos(an) * rr, y + math.sin(an) * rr))
    poli(c, pts); traco(c, w, cor, a)

# ===================================================== m01 cavando no cume (16.2)
def m01(c, cr, t):
    for x_ in (c, cr): x_.save(); cam(x_, 960, 430, 1.45 + 0.12 * ease(t / 16))
    # o cume e o chão em corte
    linha(c, [(150, 520), (700, 380), (960, 330), (1240, 380), (1770, 520)], 5)
    linha(c, [(150, 520), (1770, 520)], 2, a=0.3)
    # neve/vento
    for i in range(90):
        R = rng(i); x = (R.rand() * 2200 - t * (420 + R.rand() * 300)) % 2100 - 90; y = R.rand() * 1000
        linha(c, [(x, y), (x + 26, y - 4)], 2, a=0.35)
    # o arqueólogo cavando
    k = math.sin(t * 3.0)
    P = pose(cab=(0, -200), pesc=(0, -170), omb_e=(-30, -160), omb_d=(30, -160), cot_e=(-10, -110 + 10 * k), cot_d=(55, -120 + 10 * k),
             mao_e=(30, -70 + 20 * k), mao_d=(70, -80 + 20 * k), cint=(0, -90), barra_e=(-25, -45), barra_d=(25, -45), pe_e=(-40, 0), pe_d=(40, 0), incl=0.25)
    Q = humano(c, 860, 345, 1.0, P)
    pa0 = Q['mao_e']; linha(c, [pa0, (pa0[0] + 70, pa0[1] + 110 + 20 * k)], 5)
    # camada que não era natural
    ca = ease((t - 5.5) / 1.0)
    if ca > 0:
        linha(cr, [(820, 470), (1100, 470)], 5, AMB, ca); linha(cr, [(820, 470), (840, 520)], 3, AMB, ca * 0.7)
    # 1,5 m abaixo: três crianças sentadas (silhuetas)
    ba = ease((t - 11.6) / 1.2)
    if ba > 0:
        linha(c, [(820, 520), (820, 760), (1120, 760), (1120, 520)], 4, a=ba)
        seta(cr, (1180, 470), (1180, 740), 4, AMB, ba)
        for i, (x, s) in enumerate(((890, 0.42), (970, 0.36), (1050, 0.55))):
            Ps = pose(cab=(0, -150), pesc=(0, -125), omb_e=(-26, -118), omb_d=(26, -118), cot_e=(-34, -80), cot_d=(34, -80),
                      mao_e=(-6, -60), mao_d=(6, -60), cint=(0, -62), barra_e=(-40, -40), barra_d=(40, -40), pe_e=(-20, 0), pe_d=(20, 0), incl=0)
            humano(cr, x, 750, s, Ps, a=ba)
    for x_ in (c, cr): x_.restore()
def m01_extra(out, t):
    out = colar(out, rot('1,5 m', 80, AMB, 'Bold'), 1400, 560, ease((t - 12.2) / 0.6), 0.4)
    return out

# ===================================================== m02 de todo o império para Cusco (15.7)
def m02(c, cr, t):
    for x_ in (c, cr): x_.save(); cam(x_, 960, 540, 1.0 + 0.05 * ease(t / 15.7))
    andes(c, t, ease(t / 1.2))
    estrela(cr, *CUSCO, 34, AMB, ease((t - 0.8) / 0.6))
    origens = [(640, 140), (720, 260), (1080, 260), (1180, 420), (650, 560), (1150, 600), (820, 760), (1100, 780), (900, 980), (760, 960)]
    for i, o in enumerate(origens):
        t0 = 2.0 + i * 0.7; k = ease((t - t0) / 3.5)
        if t < t0: continue
        linha(c, [o, CUSCO], 2, a=0.25)
        p = lp(o, CUSCO, k)
        ponto(cr, p[0], p[1], 9, AMB, 1.0 if k < 1 else 0.6)
        circ(c, o[0], o[1], 10, 3, a=0.8)
    for x_ in (c, cr): x_.restore()
def m02_extra(out, t):
    out = colar(out, rot('CUSCO', 58, AMB, 'Bold'), CUSCO[0] + 190, CUSCO[1] - 50, ease((t - 1.0) / 0.6), 0.4)
    out = colar(out, rot('crianças de todo o império', 46, BR, 'Regular'), 1360, 980, ease((t - 3.0) / 0.8))
    return out

# ===================================================== m03 o caminho de Tanta Carhua (18.6)
def m03(c, cr, t):
    for x_ in (c, cr): x_.save(); cam(x_, 960, 540, 1.0 + 0.04 * ease(t / 18.6))
    V, C, M = (430, 700), (1480, 460), (520, 300)
    for x, y, txt in ((V[0], V[1], 'v'), (C[0], C[1], 'c')):
        pass
    # vilarejo
    for k in range(3): oca(c, V[0] - 80 + k * 80, V[1] + 60, 0.35)
    # Cusco
    estrela(cr, C[0], C[1], 40, AMB, 1.0)
    # montanha
    montanha(c, M[0], M[1] + 140, 360, 260)
    caminho = [(0.5, V, C, 4.0), (7.0, C, V, 4.0), (12.0, V, M, 4.5)]
    pos = V
    for t0, a_, b_, du in caminho:
        k = ease((t - t0) / du)
        if t > t0:
            linha(c, parcial(bez(a_, (a_[0], a_[1] - 220), (b_[0], b_[1] - 220), b_, 40), k), 3, a=0.6)
            if k > 0: pos = lp(a_, b_, k) if k < 1 else b_
    # festa em Cusco: faíscas
    if 4.5 < t < 7.2:
        for i in range(14):
            an = i * 0.45 + t * 2; rr = 60 + 30 * math.sin(t * 5 + i)
            ponto(cr, C[0] + math.cos(an) * rr, C[1] + math.sin(an) * rr, 4, AMB, 0.8)
    # a menina (ponto com halo)
    ponto(cr, pos[0], pos[1] - 10, 11, AMB, 1.0); circ(cr, pos[0], pos[1] - 10, 22 + 4 * math.sin(t * 4), 2, AMB, 0.6)
    for x_ in (c, cr): x_.restore()
def m03_extra(out, t):
    for txt, x, y, t0 in (('VILAREJO', 430, 860, 0.3), ('CUSCO', 1480, 560, 0.8), ('A MONTANHA', 520, 520, 11.5)):
        out = colar(out, rot(txt, 50, AMB if txt == 'CUSCO' else BR), x, y, ease((t - t0) / 0.6))
    out = colar(out, rot('SIMULAÇÃO', 30, BR, 'Regular'), 1780, 60, 0.7)
    return out

# ===================================================== m04 o diário no cabelo (régua de 24 meses)
X0, X1, YF = 260, 1660, 520     # o fio: X0 = 24 meses antes, X1 = a morte
def mx(m): return X1 - (X1 - X0) * m / 24.0   # m = meses antes da morte
def cabelo(c, cr, t, ate_fase):
    # o fio ondulado
    pts = [(x, YF + 8 * math.sin(x / 35)) for x in np.linspace(X0, X1, 220)]
    linha(c, pts, 6, a=0.95)
    for x in np.linspace(X0, X1, 220)[::3]:
        linha(c, [(x, YF + 8 * math.sin(x / 35) - 10), (x + 6, YF + 8 * math.sin(x / 35) + 10)], 1.5, a=0.3)
    # régua
    for m in range(25):
        x = mx(m); h = 26 if m % 6 == 0 else 12
        linha(c, [(x, YF + 60), (x, YF + 60 + h)], 3 if m % 6 == 0 else 2, a=0.7)
    linha(c, [(X0, YF + 60), (X1, YF + 60)], 2, a=0.5)
def m04_cena(fase, dur):
    def cena(c, cr, t):
        for x_ in (c, cr): x_.save(); cam(x_, 960, 540, 1.0 + 0.03 * ease(t / dur))
        a0 = 1.0 if fase > 0 else ease(t / 2.0)
        c.push_group(); cabelo(c, cr, t, fase); c.pop_group_to_source(); c.paint_with_alpha(a0)
        if fase == 0:   # os cortes
            for i in range(24):
                k = ease((t - 16.0 - i * 0.12) / 0.3)
                if k > 0: linha(cr, [(mx(i + 0.5), YF - 30), (mx(i + 0.5), YF + 30)], 2.5, AMB, k)
        # marcas acumuladas
        if fase >= 1:   # escolhida: -12
            k = 1.0 if fase > 1 else ease((t - 0.3) / 0.8)
            linha(cr, [(mx(12), YF - 160), (mx(12), YF + 40)], 4, AMB, k)
            if fase == 1:
                # curva da comida de elite subindo
                pts = [(mx(m), 860 - (90 if m < 12 else 0) - 10 * math.sin(m)) for m in np.linspace(24, 0, 80)]
                linha(cr, parcial(pts, ease((t - 4.0) / 3.0)), 4, AMB, 0.9)
                linha(c, [(X0, 880), (X1, 880)], 2, a=0.4)
        if fase >= 2:   # corte: -6
            k = 1.0 if fase > 2 else ease((t - 0.3) / 0.8)
            linha(cr, [(mx(6), YF - 160), (mx(6), YF + 40)], 4, AMB, k)
            if fase == 2:   # a tesoura
                sx = mx(6); a_ = ease((t - 1.0) / 0.6)
                for s in (-1, 1):
                    linha(cr, [(sx - 40, YF - 90 + s * 30 * (0.6 + 0.4 * math.sin(t * 6))), (sx + 30, YF - 90)], 5, AMB, a_)
                    circ(cr, sx - 55, YF - 90 + s * 34, 14, 4, AMB, a_)
        if fase == 3:   # a viagem: o mapa pequeno
            k = ease((t - 0.5) / 8.0)
            ox, oy, s = 1180, 690, 0.7
            P = lambda p: (ox + (p[0] - 900) * s, oy + (p[1] - 470) * s)
            linha(c, parcial(bez(P(CUSCO), P((1000, 560)), P((1080, 760)), P(LLULLA), 40), 1.0), 3, a=0.5)
            q = lp(P(CUSCO), P(LLULLA), k); ponto(cr, q[0], q[1], 10, AMB)
            estrela(cr, *P(CUSCO), 22, AMB); montanha(c, P(LLULLA)[0], P(LLULLA)[1] + 30, 130, 100)
            linha(cr, [(mx(4.5), YF - 120), (mx(0), YF - 120)], 6, AMB, 0.8 * ease((t - 0.3) / 1.0))
        if fase >= 4:   # álcool nas últimas semanas
            x8 = mx(2)
            reg = ease((t - 0.3) / 0.8)
            ret_arred(cr, x8, YF - 140, X1, YF + 40, 10); traco(cr, 4, AMB, reg)
            pico = ease((t - 4.2) / 1.0)
            pts = [(mx(m), 880 - (0 if m > 2 else 260 * pico * (1 - m / 2.0) ** 0.5) - 6 * math.sin(m * 3)) for m in np.linspace(24, 0, 120)]
            linha(cr, pts, 5, AMB, 0.95)
            linha(c, [(X0, 880), (X1, 880)], 2, a=0.4)
        for x_ in (c, cr): x_.restore()
    return cena
def m04_extra(fase, dur):
    def extra(out, t):
        z = 1.0 + 0.03 * ease(t / dur)
        P = lambda x, y: (960 + (x - 960) * z, 540 + (y - 540) * z)
        out = colar(out, rot('24 MESES', 40, BR, 'Regular'), *P(X0, YF + 130), 0.8)
        out = colar(out, rot('A MORTE', 40, BR, 'Regular'), *P(X1, YF + 130), 0.8)
        if fase == 0:
            out = colar(out, rot('1 cm ≈ 1 mês', 64, AMB, 'Bold'), *P(960, 300), ease((t - 5.0) / 0.8), 0.4)
        if fase >= 1:
            big = fase == 1
            out = colar(out, rot('ESCOLHIDA' if big else '-12 meses', 50 if big else 34, AMB, 'Bold'), *P(mx(12), YF - 200), 1.0 if not big else ease((t - 0.6) / 0.6), 0.3)
        if fase == 1:
            out = colar(out, rot('carne + milho: comida de elite', 44, BR, 'Regular'), *P(960, 960), ease((t - 4.0) / 0.8))
        if fase >= 2:
            big = fase == 2
            out = colar(out, rot('CABELO CORTADO' if big else '-6 meses', 50 if big else 34, AMB, 'Bold'), *P(mx(6), YF - (260 if big else 200)), 1.0 if not big else ease((t - 0.6) / 0.6), 0.3)
        if fase == 3:
            out = colar(out, rot('1.420 km', 70, AMB, 'Bold'), *P(1560, 860), ease((t - 1.0) / 0.6), 0.4)
            out = colar(out, rot('A VIAGEM', 50, AMB, 'Bold'), *P(mx(2.2), YF - 260), ease((t - 0.6) / 0.6), 0.3)
        if fase >= 4:
            out = colar(out, rot('ÚLTIMAS 6–8 SEMANAS', 46, AMB, 'Bold'), *P(1440, YF - 260), ease((t - 0.6) / 0.6), 0.3)
            out = colar(out, rot('ÁLCOOL', 80, AMB, 'Bold'), *P(1330, 760), ease((t - 4.4) / 0.5), 0.6)
        return out
    return extra

# ===================================================== m05 a câmara de pedra (SIMULAÇÃO, 14.1)
def m05(c, cr, t):
    for x_ in (c, cr): x_.save(); cam(x_, 960, 560, 1.0 + 0.1 * ease(t / 14))
    linha(c, [(200, 380), (760, 300), (960, 270), (1180, 300), (1720, 380)], 5)
    # câmara
    for i in range(7):
        linha(c, [(780 + i * 4, 420 + i * 40), (790 + i * 4, 450 + i * 40)], 3, a=0.5)
        linha(c, [(1140 - i * 4, 420 + i * 40), (1130 - i * 4, 450 + i * 40)], 3, a=0.5)
    ret_arred(c, 780, 400, 1140, 720, 20); traco(c, 5)
    Ps = pose(cab=(0, -150), pesc=(0, -125), omb_e=(-26, -118), omb_d=(26, -118), cot_e=(-34, -80), cot_d=(34, -80),
              mao_e=(-6, -60), mao_d=(6, -60), cint=(0, -62), barra_e=(-40, -40), barra_d=(40, -40), pe_e=(-20, 0), pe_d=(20, 0), incl=0.12 * ease(t / 12))
    humano(c, 960, 700, 1.25, Ps)
    # respiração ficando lenta
    per = 2.0 + 3.0 * ease(t / 12)
    fa = 1 - ease((t - 11.5) / 1.5)
    f = (t % per) / per
    if f < 0.4 and fa > 0:
        for k in range(3):
            circ(c, 1000 + f * 140 + k * 18, 520 - f * 40 - k * 8, 8 + f * 30, 2, a=(0.4 - f) * 1.8 * fa)
    # flocos de neve caindo
    for i in range(60):
        R = rng(i); x = R.rand() * 1920; y = (R.rand() * 1100 + t * (40 + 30 * R.rand())) % 1100
        ponto(c, x, y, 3, a=0.5)
    # termômetro
    tx, ty = 1450, 420
    ret_arred(c, tx - 16, ty - 200, tx + 16, ty + 120, 14); traco(c, 4)
    circ(c, tx, ty + 150, 36, 4)
    nivel = ty + 110 - 260 * (1 - ease(t / 12))
    linha(cr, [(tx, ty + 120), (tx, nivel)], 10, AMB, 0.9)
    for x_ in (c, cr): x_.restore()
def m05_extra(out, t):
    return colar(out, rot('SIMULAÇÃO', 30, BR, 'Regular'), 1780, 60, 0.7)

# ===================================================== m06 os santuários (8.2)
PICOS = [(700, 160), (760, 290), (820, 420), (880, 540), (930, 650), (960, 770), (990, 880), (1010, 990)]
def m06(c, cr, t):
    for x_ in (c, cr): x_.save(); cam(x_, 960, 540, 1.0 + 0.04 * ease(t / 8))
    andes(c, t)
    for i, (x, y) in enumerate(PICOS):
        k = ease((t - 0.4 - i * 0.55) / 0.5)
        if k > 0:
            ponto(cr, x + 40, y - 30, 10, AMB, k); circ(cr, x + 40, y - 30, 24 + 6 * math.sin(t * 3 + i), 2, AMB, 0.6 * k)
    for x_ in (c, cr): x_.restore()
def m06_extra(out, t):
    for txt, x, y, t0 in (('AMPATO (Peru)', 1180, 510, 0.4), ('LLULLAILLACO (Argentina)', 1330, 740, 1.5), ('EL PLOMO (Chile)', 1310, 960, 2.6)):
        out = colar(out, rot(txt, 44, AMB, 'Bold'), x, y, ease((t - t0) / 0.6), 0.3)
    return out

# ===================================================== m07 o império amarrado (18.6)
def m07(c, cr, t):
    for x_ in (c, cr): x_.save(); cam(x_, 960, 540, 1.0 + 0.06 * ease(t / 18.6))
    andes(c, t, 0.7)
    estrela(cr, *CUSCO, 36, AMB)
    origens = [(640, 140), (720, 260), (1080, 260), (1180, 420), (650, 560), (1150, 600), (820, 760), (1100, 780), (900, 980), (760, 960)]
    for i, o in enumerate(origens):
        t0 = 0.5 + i * 0.9
        k1 = ease((t - t0) / 1.6); k2 = ease((t - t0 - 1.8) / 1.6)
        if k1 > 0:
            linha(c, parcial([o, CUSCO], k1), 3, a=0.7)          # a criança vai a Cusco
        if k2 > 0:
            linha(cr, parcial([CUSCO, o], k2), 4, AMB, 0.9)      # e volta, para a montanha da própria província
            montanha(cr, o[0], o[1] + 18, 46, 40, k2, AMB, False, 3)
    # no fim, a "rede" pulsa
    if t > 13.0:
        p = 0.5 + 0.5 * math.sin(t * 4)
        circ(cr, *CUSCO, 70 + 30 * p, 3, AMB, 0.5)
    for x_ in (c, cr): x_.restore()
def m07_extra(out, t):
    out = colar(out, rot('CUSCO', 58, AMB, 'Bold'), CUSCO[0] + 190, CUSCO[1] - 50, 1.0, 0.4)
    out = colar(out, rot('cada província entrega uma criança', 46, BR, 'Regular'), 1360, 980, ease((t - 1.0) / 0.8))
    return out

ANIMS = {
    'm01': (m01, 16.2, 'anim-m01-cavando', m01_extra),
    'm02': (m02, 15.7, 'anim-m02-para-cusco', m02_extra),
    'm03': (m03, 18.6, 'anim-m03-tanta-carhua', m03_extra),
    'm04a': (m04_cena(0, 20.6), 20.6, 'anim-m04a-regua', m04_extra(0, 20.6)),
    'm04b': (m04_cena(1, 13.8), 13.8, 'anim-m04b-escolhida', m04_extra(1, 13.8)),
    'm04c': (m04_cena(2, 8.9), 8.9, 'anim-m04c-corte', m04_extra(2, 8.9)),
    'm04d': (m04_cena(3, 10.6), 10.6, 'anim-m04d-viagem', m04_extra(3, 10.6)),
    'm04e': (m04_cena(4, 20.4), 20.4, 'anim-m04e-alcool', m04_extra(4, 20.4)),
    'm05': (m05, 14.1, 'anim-m05-camara', m05_extra),
    'm06': (m06, 8.2, 'anim-m06-santuarios', m06_extra),
    'm07': (m07, 18.6, 'anim-m07-imperio', m07_extra),
}

if __name__ == '__main__':
    modo, nome = sys.argv[1], sys.argv[2]
    nomes = list(ANIMS) if nome == 'todos' else nome.split(',')
    for n in nomes:
        cena, dur, arq, ex = ANIMS[n]
        if modo == 'teste':
            quadros(cena, [float(x) for x in sys.argv[3].split(',')], 'tst/' + n, ex)
        else:
            render(cena, dur, f'out/{arq}.mp4', extra=ex)
            print('pronto', n, flush=True)
