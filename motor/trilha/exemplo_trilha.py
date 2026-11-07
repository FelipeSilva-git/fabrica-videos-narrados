"""Trilha original — A menina que dormiu por 500 anos (Llullaillaco).
Duas saídas: trilha.wav (música contínua) e fx.wav (efeitos das cenas e animações).
Também grava tensao.json (curva do fundo). Tempos absolutos do vídeo final (tempos.json)."""
import sys, os, json, wave, re
import numpy as np
from scipy.signal import fftconvolve
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from sfx_lib import *

# uso: python3 exemplo_trilha.py <pasta_do_episodio> [pasta_de_saida]
# precisa de: <pasta>/tempos.json (scripts/linha_do_tempo.py), N-ritmo.alinhamento.json e storyboard-parteN.txt
RE = sys.argv[1] if len(sys.argv) > 1 else '.'
AQUI = sys.argv[2] if len(sys.argv) > 2 else RE
TP = json.load(open(f'{RE}/tempos.json'))
FIM = TP['FIM']
N = int(FIM * SR); t = np.arange(N) / SR
def T(p, i, fim=False): return TP[str(p)]['tr'][i - 1][1 if fim else 0]

class Faixa:
    def __init__(s): s.L = np.zeros(N, np.float32); s.R = np.zeros(N, np.float32)
    def put(s, sig, t0, gl=1.0, gr=None):
        i = int(t0 * SR); gr = gl if gr is None else gr
        if i < 0: sig = sig[-i:]; i = 0
        j = min(N, i + len(sig))
        if j > i: s.L[i:j] += sig[:j - i] * gl; s.R[i:j] += sig[:j - i] * gr
M = Faixa(); FX = Faixa()
def env(pts):
    xs, ys = zip(*pts); return np.interp(t, xs, ys).astype(np.float32)

# ============================================================ MAPA
AC = {'Am': [33, 45, 48, 52], 'G': [43, 55, 59, 62], 'Em': [40, 52, 55, 59], 'C': [36, 48, 52, 55], 'Am': [33, 45, 48, 52], 'B': [35, 47, 51, 54], 'D': [38, 50, 54, 57],
      'F': [41, 53, 57, 60], 'Dm': [38, 50, 53, 57], 'E': [40, 52, 56, 59], 'G': [43, 55, 59, 62]}
B1, B2, B3, B4, B5, B6 = T(1, 6), T(2, 1), T(3, 1), T(4, 1), T(5, 1), T(6, 1)
VI = T(5, 5); FECHA = T(6, 6)
SECOES = [
    (0.0, B1, ['Am', 'F', 'C', 'E'], 6.0, 1000),
    (B1, B2, ['Am', 'G', 'F', 'E'], 5.0, 1400),
    (B2, B3, ['Am', 'C', 'G', 'Am'], 5.5, 1500),
    (B3, B4, ['Dm', 'Am', 'F', 'E'], 6.5, 1100),
    (B4, B5, ['Am', 'F', 'Dm', 'E'], 4.5, 1600),
    (B5, VI, ['Dm', 'Am', 'E', 'Am'], 6.0, 1000),
    (VI, B6, ['Am', 'G', 'F', 'E'], 5.0, 1300),
    (B6, FECHA, ['Am', 'F', 'Dm', 'E'], 5.0, 1300),
    (FECHA, FIM, ['Am', 'F', 'C', 'G'], 6.0, 1200),
]
IMP = [T(1, 3), T(1, 9), T(2, 5), T(3, 3), T(4, 5), T(4, 11), T(4, 15), T(6, 3), T(6, 6)]
bur = [(0, 1)]
for x in IMP: bur += [(x - 0.05, 1), (x + 0.08, 0.08), (x + 1.3, 0.1), (x + 2.4, 1)]
s8 = T(3, 3)   # a frase de Tanta Carhua quase sem música
bur += [(s8 - 0.2, 1), (s8 + 0.3, 0.15), (T(3, 4) - 0.1, 0.15), (T(3, 4) + 1.0, 1)]
buraco = env(sorted(bur) + [(FIM, 1)])

# curva de tensão (fundo e cama)
TEN = [(0, 0.6), (T(1, 3), 0.7), (T(1, 4), 0.55), (T(1, 6), 0.45), (T(1, 7), 0.55), (T(1, 8), 0.75), (T(1, 9), 0.85), (T(1, 12), 0.6), (T(1, 13), 0.7),
       (T(2, 1), 0.45), (T(2, 3), 0.5), (T(2, 5), 0.65), (T(2, 6), 0.5),
       (T(3, 1), 0.55), (T(3, 2), 0.65), (T(3, 3), 0.8), (T(3, 4), 0.85), (T(3, 6), 0.45),
       (T(4, 1), 0.6), (T(4, 3), 0.65), (T(4, 5), 0.8), (T(4, 7), 0.75), (T(4, 9), 0.8), (T(4, 10), 0.9), (T(4, 11), 1.0), (T(4, 13), 0.85), (T(4, 15), 0.9),
       (T(5, 1), 0.7), (T(5, 2), 0.8), (T(5, 3), 0.75), (T(5, 5), 0.45), (T(5, 7), 0.55),
       (T(6, 1), 0.6), (T(6, 2), 0.75), (T(6, 3), 0.85), (T(6, 4), 0.6), (T(6, 5), 0.45), (T(6, 6), 0.4), (T(6, 8), 0.3), (T(6, 9), 0.25), (FIM, 0.0)]
json.dump([[round(a, 2), b] for a, b in TEN], open(f'{RE}/tensao.json', 'w'))
inten = env([(a, min(1.0, 0.35 + 0.75 * b)) for a, b in TEN])

# ============================================================ 1. CAMA (contínua)
for (a, b, prog, passo, corte) in SECOES:
    tm = a; k = 0
    while tm < b - 0.5:
        d = min(passo, b - tm) + 1.5
        M.put(pad(AC[prog[k % len(prog)]], d, 0.5, corte, ataque=1.2, solta=1.6), tm, 0.9, 1.0); tm += passo; k += 1
    tonica = AC[prog[0]][0]
    M.put(pad([tonica - 12 if tonica > 36 else tonica], b - a + 2, 0.35, 220, 2.0, 2.0), a)
cama_env = (0.45 + 0.55 * inten) * buraco
M.L *= cama_env; M.R *= cama_env

def amostra(env_, tm): return float(np.interp(tm, t[::SR // 10], env_[::SR // 10]))

# ============================================================ 2. DEDILHADO (cordas) nos blocos narrativos
def arpejo(a, b, prog, passo, bpm, g=0.09):
    tm = a; i = 0; dt = 60 / bpm / 2
    while tm < b:
        ac = AC[prog[int((tm - a) // passo) % len(prog)]]
        m = ac[1:][[0, 1, 2, 1][i % 4]] + 12
        M.put(pluck(m, 1.8, g * (1.0 if i % 4 == 0 else 0.7), 0.4) * amostra(buraco, tm), tm, 0.7 + 0.3 * (i % 2), 1.0 - 0.3 * (i % 2))
        tm += dt; i += 1
arpejo(T(1, 6), T(1, 8), ['Am', 'G', 'F', 'E'], 5.0, 96, 0.08)
arpejo(T(2, 1), T(2, 5), ['Am', 'C', 'G', 'Am'], 5.5, 104, 0.09)
arpejo(T(4, 3), T(4, 10), ['Am', 'F', 'Dm', 'E'], 4.5, 88, 0.07)
arpejo(T(6, 6), FIM, ['Am', 'F', 'C', 'G'], 6.0, 72, 0.07)

# ============================================================ 3. PERCUSSÃO (tambor, taiko, maracá)
def maraca(g=0.06):
    n = int(0.09 * SR); e = np.exp(-np.arange(n) / SR * 40).astype(np.float32)
    return bp(ruido(n), 3000, 9000) * e * g
def ritmo(a, b, bpm0, bpm1, g0, tipo='tambor', padrao=(1, 0, 0.6, 0, 0.8, 0, 0.6, 0.4)):
    tm = a; i = 0
    while tm < b:
        p = (tm - a) / max(b - a, 1e-3); bpm = bpm0 + (bpm1 - bpm0) * p; v = padrao[i % len(padrao)]
        if v:
            if tipo == 'maraca': s = maraca(g0 * v)
            elif tipo == 'taiko': s = taiko(g0 * v * (0.7 + 0.5 * p))
            elif tipo == 'coracao': s = coracao(g0 * v)
            else: s = tambor(g0 * v * (0.7 + 0.5 * p))
            M.put(s * amostra(buraco, tm), tm, 0.95, 1.0)
        tm += 60 / bpm / 2; i += 1
ritmo(T(1, 8), T(1, 9) - 0.2, 66, 90, 0.2, 'taiko', (1, 0, 0, 0, 0.6, 0, 0, 0))          # cavando
ritmo(T(2, 2), T(2, 4), 84, 84, 0.16, 'tambor', (1, 0, 0, 0.5, 0.8, 0, 0, 0))            # procissão: bombo
ritmo(T(2, 2), T(2, 4), 168, 168, 0.35, 'maraca', (1, 0, 0.6, 0))
ritmo(T(4, 5), T(4, 10), 60, 60, 0.22, 'coracao', (1, 0, 0, 0))                           # o diário: pulso
ritmo(T(4, 10), T(4, 13), 90, 150, 0.24, 'taiko', (1, 0, 0, 0, 0.8, 0, 0, 0))             # o álcool dispara
ritmo(T(6, 2), T(6, 4), 70, 110, 0.22, 'tambor', (1, 0, 0.5, 0, 0.9, 0, 0.5, 0))         # o império amarrado

# ============================================================ 4. MELODIA (flauta) e CORO
for t0, nt, du, g in ((T(1, 1) + 0.6, [69, 72, 74, 72, 69], [0.8, 0.6, 1.2, 0.6, 2.8], 0.04),
                      (T(1, 6) + 0.3, [69, 71, 72, 76, 74, 72, 71, 69], [0.5, 0.4, 0.5, 1.0, 0.5, 0.5, 0.6, 2.4], 0.045),
                      (T(2, 3) + 0.3, [76, 74, 72, 74, 76, 79, 76], [0.5, 0.4, 0.6, 0.5, 0.6, 1.0, 2.6], 0.045),
                      (T(3, 2) + 0.4, [74, 72, 69, 68, 69], [0.7, 0.6, 0.9, 0.7, 2.8], 0.04),
                      (T(5, 5) + 0.3, [69, 72, 71, 69, 64], [0.6, 0.6, 0.8, 0.6, 2.6], 0.04),
                      (T(6, 6) + 0.5, [69, 72, 74, 76, 72, 69], [0.8, 0.6, 0.8, 1.4, 0.8, 3.2], 0.04)):
    M.put(ney(nt, du, g), t0, 0.85, 1.0)
for a, b, nt, g in ((T(1, 9), T(1, 11), [45, 52, 57, 60], 0.45), (T(3, 3), T(3, 5), [50, 57, 62, 65], 0.35), (T(4, 15), T(5, 1), [45, 52, 57, 64], 0.5),
                    (T(6, 6), FIM, [45, 52, 57, 60, 64], 0.45)):
    M.put(coro(nt, b - a, g, ataque=1.5, solta=2.0), a, 0.95, 1.0)

# ============================================================ 5. SINOS, IMPACTOS E SUBIDAS
M.put(sino_grave(0.18), 0.3)
for x, g in zip(IMP, (0.6, 0.6, 0.4, 0.5, 0.7, 0.8, 0.5, 0.6, 0.4)):
    g *= 0.4; M.put(impacto(g), x + 0.06); M.put(subida(2.0, g * 0.35), x - 1.9)
for tm in (B1, B2, B3, B4, B5, B6):
    M.put(subida(2.6, 0.15), tm - 2.4)

# ============================================================ 6. EFEITOS (fx.wav)
def _inicios():
    out = {}
    for p in range(1, 7):
        al = json.load(open(f'{RE}/{p}-ritmo.alinhamento.json'))['trechos']
        off = TP[str(p)]['off']; atual = None; anc = None
        for ln in open(f'{RE}/storyboard-parte{p}.txt', encoding='utf-8'):
            m = re.match(r'\s*\[(\d+)\]', ln)
            if m: atual = int(m.group(1)); anc = None; continue
            if ln.strip().startswith('+'): anc = ln.strip()[1:].strip(); continue
            mv = re.match(r'\s*video:\s*videos/((?:anim|clip)-[\w-]+)\.mp4', ln)
            if mv and atual:
                tr = al[atual - 1]; a_, b_ = tr['inicio'], tr['fim']
                if anc:
                    pos = tr['texto'].lower().find(anc.lower()); a_ = a_ + (b_ - a_) * (pos / max(1, len(tr['texto'])))
                out.setdefault(mv.group(1), round(off + max(0.0, a_ - 0.15), 2))
    return out
A = _inicios()
print('inícios:', A)
def an(pref): return [v for k, v in A.items() if k.startswith(pref)][0]
# o cume: vento constante na abertura e no bloco I
FX.put(vento(18, 0.06), 0.0); FX.put(vento(30, 0.07), T(1, 6))
s0 = an('anim-m01')
for k in range(9): FX.put(baque(0.06, 160), s0 + 0.5 + k * 1.05)   # a pá
FX.put(sino_grave(0.12), s0 + 11.6)
FX.put(multidao(14, 0.12, 0.5), T(2, 3))                          # festas em Cusco
s0 = an('anim-m03')
for k in range(14): FX.put(clique(0.03, 1800), s0 + 0.6 + k * 0.32)  # passos
FX.put(multidao(5, 0.12, 0.6), s0 + 4.6)
FX.put(vento(10, 0.05), T(3, 4)); FX.put(baque(0.12, 70), T(3, 4) + 6.0)   # a pedra fechando
s0 = an('anim-m04a')
for k in range(24): FX.put(clique(0.05, 2600), s0 + 16.0 + k * 0.12)       # os cortes no fio
for nm in ('anim-m04b', 'anim-m04c', 'anim-m04d', 'anim-m04e'): FX.put(sino(88, 0.04, 2.5), an(nm) + 0.3)
FX.put(whoosh(1.0, 0.09, 200, 3000), an('anim-m04e') + 4.0)
s0 = an('anim-m05'); FX.put(vento(14, 0.07), s0)
s0 = an('anim-m06')
for k in range(8): FX.put(sino(76 + k, 0.025, 2), s0 + 0.4 + k * 0.55)
s0 = an('anim-m07'); FX.put(whoosh(0.8, 0.05, 300, 2500), s0 + 1.0)
FX.put(vento(16, 0.05), T(6, 6))

# ============================================================ reverb e master
def reverb(F, mix=0.5, dur=3.4, dec=1.8):
    ir_t = np.arange(int(dur * SR)) / SR
    for ch in (F.L, F.R):
        ir = (ruido(len(ir_t)) * np.exp(-ir_t * dec)).astype(np.float32); ir /= np.sqrt((ir ** 2).sum())
        ch[:] = ch * 0.75 + fftconvolve(ch, ir)[:N].astype(np.float32) * mix
def salvar(F, nome, pico=0.9, fade=4.0):
    mix = np.stack([F.L, F.R], 1); mix = np.tanh(mix * 1.2) / 1.2
    mix *= np.clip((FIM - t) / fade, 0, 1)[:, None]
    if pico: mix /= np.abs(mix).max() / pico
    print(nome, 'pico', round(float(np.abs(mix).max()), 3))
    with wave.open(nome, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
reverb(M, 0.5); reverb(FX, 0.25, 1.6, 3.5)
salvar(M, f'{AQUI}/trilha.wav')
salvar(FX, f'{AQUI}/fx.wav', None)
