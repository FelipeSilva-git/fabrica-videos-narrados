"""Biblioteca de efeitos sonoros e instrumentos sintetizados (sem arquivos de fora).
Tudo devolve arrays float32 mono a 44,1 kHz. Use com uma função put(sinal, t0, gl, gr) da trilha."""
import numpy as np
from scipy.signal import butter, sosfilt, lfilter

SR = 44100
_rng = np.random.default_rng(7)

def ruido(n): return _rng.standard_normal(int(n)).astype(np.float32)
def lp(x, f, o=2): return sosfilt(butter(o, min(f, SR / 2 - 100) / (SR / 2), output='sos'), x).astype(np.float32)
def hp(x, f, o=2): return sosfilt(butter(o, f / (SR / 2), 'high', output='sos'), x).astype(np.float32)
def bp(x, a, b, o=2): return sosfilt(butter(o, [a / (SR / 2), min(b, SR / 2 - 100) / (SR / 2)], 'band', output='sos'), x).astype(np.float32)
def hz(m): return 440 * 2 ** ((m - 69) / 12)
def tt(d): return np.arange(int(d * SR)) / SR
def env_ar(n, a, r):
    t = np.arange(n) / SR; d = n / SR
    return (np.minimum(1, t / max(a, 1e-3)) * np.clip((d - t) / max(r, 1e-3), 0, 1)).astype(np.float32)

# ---------------------------------------------------------------- instrumentos
def pluck(m, d=2.5, g=0.3, brilho=0.5, decai=0.996):
    """corda dedilhada (oud/harpa), Karplus-Strong"""
    f = hz(m); N = max(2, int(SR / f)); n = int(d * SR)
    x = np.zeros(n, np.float32); x[:N] = lp(ruido(N), 1500 + 6000 * brilho)
    a = np.zeros(N + 2); a[0] = 1; a[N] = -decai / 2; a[N + 1] = -decai / 2
    y = lfilter([1.0], a, x).astype(np.float32)
    return y / (np.abs(y).max() + 1e-6) * g * env_ar(n, 0.002, 0.3)

def pad(notas, d, g=0.1, corte=1800, ataque=2.0, solta=2.5, detune=0.006):
    """cordas/sintetizador: serras desafinadas filtradas"""
    t = tt(d); s = np.zeros(len(t), np.float32)
    for m in notas:
        f0 = hz(m)
        for k in (-1, 0, 1):
            f = f0 * (1 + k * detune)
            ph = (f * t + _rng.random()) % 1.0
            s += (2 * ph - 1).astype(np.float32)
    s = lp(lp(s, corte), corte * 1.2)
    return s / (len(notas) * 3) * g * env_ar(len(t), ataque, solta)

def ney(notas, durs, g=0.05):
    tot = sum(durs); n = int((tot + 1.5) * SR); t = np.arange(n) / SR
    f = np.zeros(n, np.float32); a = np.zeros(n, np.float32); acc = 0
    for m, d in zip(notas, durs):
        i0, i1 = int(acc * SR), int((acc + d) * SR); f[i0:i1] = hz(m); a[i0:i1] = 1; acc += d
    f[int(acc * SR):] = hz(notas[-1])
    f = lp(np.maximum(f, 1), 18); a = lp(a, 6) * np.minimum(1, t / 0.15)
    vib = 1 + 0.008 * np.sin(2 * np.pi * 5.2 * t) * np.minimum(1, t / 0.6)
    fase = 2 * np.pi * np.cumsum(f * vib) / SR
    s = np.sin(fase) + 0.18 * np.sin(2 * fase) + 0.06 * np.sin(3 * fase) + bp(ruido(n), 600, 3000) * 0.35
    return (s * a * g).astype(np.float32)

FORM = [(700, 1.0, 110), (1150, 0.55, 120), (2600, 0.25, 160)]
def coro(notas, d, g=0.05, ataque=3.0, solta=3.0):
    t = tt(d); s = np.zeros(len(t), np.float32)
    for m in notas:
        f0 = hz(m)
        for v in range(3):
            fv = f0 * (1 + (v - 1) * 0.004)
            fase = 2 * np.pi * np.cumsum(fv * (1 + 0.006 * np.sin(2 * np.pi * (5 + v * 0.3) * t + v))) / SR
            for k in range(1, 14):
                fk = fv * k
                a = sum(amp * np.exp(-((fk - fc) / bw) ** 2) for fc, amp, bw in FORM) + 0.08 / k
                if a < 0.01: continue
                s += (np.sin(k * fase + _rng.random() * 6) * a).astype(np.float32)
    return s * g / (len(notas) * 3) * env_ar(len(t), ataque, solta)

def sino(m, g=0.08, d=4.0):
    t = tt(d); f = hz(m)
    s = sum(a * np.sin(2 * np.pi * f * r * t) * np.exp(-t * (1.2 + r * 0.6)) for r, a in ((1, 1.0), (2.76, 0.5), (5.4, 0.25), (8.93, 0.12)))
    return (s * g).astype(np.float32)

def sino_grave(g=0.3, d=7.0):
    t = tt(d); f = 55
    s = sum(a * np.sin(2 * np.pi * f * r * t) * np.exp(-t * (0.5 + r * 0.25)) for r, a in ((1, 1.0), (2.0, 0.6), (2.98, 0.4), (4.1, 0.25), (5.4, 0.15)))
    return (s * g).astype(np.float32)

# ---------------------------------------------------------------- percussão
def tambor(g=0.3, f0=95):
    t = tt(0.6); f = f0 * np.exp(-t * 9) + 52
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7)
    s += bp(ruido(len(t)), 400, 2500) * np.exp(-t * 40) * 0.4
    return (s * g).astype(np.float32)

def taiko(g=0.5):
    t = tt(1.4); f = 70 * np.exp(-t * 6) + 38
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 3.5)
    s += lp(ruido(len(t)), 900) * np.exp(-t * 18) * 0.5
    return (s * g).astype(np.float32)

def bumbo(g=0.3):
    t = tt(0.5); f = 80 * np.exp(-t * 12) + 45
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9) * g).astype(np.float32)

def coracao(g=0.35):
    return np.concatenate([bumbo(g), np.zeros(int(0.02 * SR), np.float32)])[:int(0.45 * SR)] + \
        np.pad(bumbo(g * 0.6), (int(0.22 * SR), 0))[:int(0.45 * SR)]

def palma(g=0.2):
    t = tt(0.12); s = bp(ruido(len(t)), 900, 5000) * np.exp(-t * 45)
    return (s * g).astype(np.float32)

def pandeiro(g=0.12):
    t = tt(0.25); s = bp(ruido(len(t)), 5000, 12000) * np.exp(-t * 18)
    return (s * g).astype(np.float32)

# ---------------------------------------------------------------- efeitos
def impacto(g=0.6, d=3.5):
    t = tt(d); f = 55 * np.exp(-t * 1.2) + 28
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 1.4) + lp(ruido(len(t)), 400) * np.exp(-t * 3) * 0.6
    return (s * g).astype(np.float32)

def subida(d=2.5, g=0.25):
    t = tt(d); return (bp(ruido(len(t)), 300, 5000) * (t / d) ** 3 * g).astype(np.float32)

def whoosh(d=0.8, g=0.25, a=300, b=4000):
    t = tt(d); return (bp(ruido(len(t)), a, b) * np.sin(np.pi * t / d) ** 2 * g).astype(np.float32)

def fogo(d, g=0.2, forca=1.0):
    """fogo contínuo: ronco grave + estalos"""
    n = int(d * SR); s = lp(ruido(n), 350) * 1.6 * forca
    s += bp(ruido(n), 800, 3000) * (0.3 + 0.2 * np.sin(np.arange(n) / SR * 3.1)) * 0.5
    est = np.zeros(n, np.float32)
    for i in _rng.integers(0, n, int(d * 18 * forca)): est[i] = _rng.uniform(-1, 1)
    s += hp(est, 1500) * 5
    return (s * g * env_ar(n, 0.4, 0.8)).astype(np.float32)

def fogo_explosao(g=0.6):
    n = int(3.0 * SR)
    out = impacto(g, 3.0)
    out[int(0.05 * SR):] += fogo(4.0, g * 0.6, 1.8)[:n - int(0.05 * SR)]
    w = whoosh(1.0, g * 0.6, 150, 3000); out[:len(w)] += w
    return out

def clink(g=0.15, base=None):
    """metal pequeno (joia, moeda): parciais inarmônicos"""
    base = base or _rng.uniform(2600, 4200); t = tt(0.6)
    s = sum(a * np.sin(2 * np.pi * base * r * t + _rng.random() * 6) * np.exp(-t * (14 + 10 * r)) for r, a in ((1, 1), (1.47, 0.6), (2.09, 0.4), (2.56, 0.3)))
    return (s * g).astype(np.float32)

def moedas(n=8, d=1.0, g=0.15):
    out = np.zeros(int((d + 0.7) * SR), np.float32)
    for k in range(n):
        i = int(_rng.uniform(0, d) * SR); c = clink(g * _rng.uniform(0.5, 1)); out[i:i + len(c)] += c[:len(out) - i]
    return out

def clique(g=0.2, f=3000, d=0.05):
    t = tt(d); return (bp(ruido(len(t)), f * 0.6, min(f * 1.6, 18000)) * np.exp(-t * 90) * g).astype(np.float32)

def baque(g=0.3, f0=70):
    t = tt(0.8); s = np.sin(2 * np.pi * np.cumsum(f0 * np.exp(-t * 3) + 30) / SR) * np.exp(-t * 6)
    return (s * g).astype(np.float32)

def multidao(d, g=0.15, agito=0.5):
    """murmúrio de muita gente (sem palavras): sílabas filtradas"""
    n = int(d * SR); s = np.zeros(n, np.float32)
    for v in range(14):
        f1 = _rng.uniform(400, 900); f2 = _rng.uniform(1100, 2200)
        sil = (np.sin(2 * np.pi * _rng.uniform(3, 6) * np.arange(n) / SR + _rng.random() * 6) > 0.2).astype(np.float32)
        sil = lp(sil, 12) * (0.5 + 0.5 * np.sin(2 * np.pi * _rng.uniform(0.1, 0.4) * np.arange(n) / SR + v))
        s += (bp(ruido(n), f1 * 0.8, f1 * 1.2) + bp(ruido(n), f2 * 0.9, f2 * 1.1) * 0.5) * sil
    s = lp(s, 2500 + 2000 * agito)
    return (s / 14 * g * 3 * env_ar(n, 0.8, 1.0)).astype(np.float32)

def moer(d, g=0.2):
    n = int(d * SR); m = 0.5 + 0.5 * np.sin(2 * np.pi * 1.6 * np.arange(n) / SR) ** 2
    s = bp(ruido(n), 150, 900) * m + bp(ruido(n), 2000, 6000) * m * 0.3
    return (s * g * env_ar(n, 0.2, 0.4)).astype(np.float32)

def agua(g=0.2, d=1.5):
    n = int(d * SR); t = np.arange(n) / SR
    s = bp(ruido(n), 300, 3000) * np.exp(-t * 4)
    for k in range(10):
        t0 = _rng.uniform(0.05, d * 0.8); f = _rng.uniform(500, 1400)
        i = int(t0 * SR); m = int(0.06 * SR)
        if i + m < n:
            tb = np.arange(m) / SR; s[i:i + m] += np.sin(2 * np.pi * (f + 4000 * tb) * tb) * np.exp(-tb * 60) * 0.3
    return (s * g).astype(np.float32)

def vento(d, g=0.12, alto=False):
    n = int(d * SR); s = bp(ruido(n), 200, 900) + (bp(ruido(n), 900, 3000) * 0.5 if alto else 0)
    m = 0.6 + 0.4 * np.sin(2 * np.pi * 0.17 * np.arange(n) / SR) * np.sin(2 * np.pi * 0.05 * np.arange(n) / SR + 1)
    return (s * m * g * env_ar(n, 1.0, 1.5)).astype(np.float32)

def pagina(g=0.12):
    t = tt(0.18); return (bp(ruido(len(t)), 1500, 7000) * np.sin(np.pi * t / 0.18) * g).astype(np.float32)

def rachar(g=0.3):
    out = np.zeros(int(1.2 * SR), np.float32)
    for k in range(9):
        i = int(_rng.uniform(0, 0.9) * SR); c = clique(g * _rng.uniform(0.5, 1), _rng.uniform(1500, 5000), 0.04); out[i:i + len(c)] += c
    out += np.pad(baque(g * 0.6, 120), (0, len(out)))[:len(out)]
    return out

def areia(d, g=0.12):
    n = int(d * SR); return (hp(ruido(n), 3000) * env_ar(n, 0.1, d * 0.6) * g).astype(np.float32)

def grilos(d, g=0.03):
    n = int(d * SR); t = np.arange(n) / SR
    gate = (np.sin(2 * np.pi * 2.3 * t) > 0.6) * (np.sin(2 * np.pi * 37 * t) > 0)
    return (np.sin(2 * np.pi * 4300 * t) * gate * g * env_ar(n, 1, 1)).astype(np.float32)

def botao(g=0.25):
    out = np.zeros(int(0.15 * SR), np.float32)
    c1 = clique(g, 2500, 0.03); c2 = clique(g * 0.6, 1200, 0.03)
    out[:len(c1)] += c1; i = int(0.07 * SR); out[i:i + len(c2)] += c2
    return out

def triste(g=0.2):
    """'não saiu nada': dois tons descendo (máquina)"""
    t = tt(0.9); f = np.where(t < 0.4, 330, 250)
    s = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * 0.4 * np.exp(-((t % 0.45) * 4))
    return (lp(s.astype(np.float32), 1800) * g).astype(np.float32)
