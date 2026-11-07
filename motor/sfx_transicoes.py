#!/usr/bin/env python3
"""Sons das transições (whoosh, impacto, flash, glitch), no tempo certo do vídeo final.
   python3 sfx_transicoes.py --parte "paralisia/2.transicoes.json:114.31" ... --duracao 367.5 --saida sfx.wav
   (o número depois de ':' é onde aquela parte começa no vídeo final)"""
import argparse, json, wave
import numpy as np
from scipy.signal import butter, sosfilt
SR = 48000
rng = np.random.default_rng(3)
def bp(x, a, b): return sosfilt(butter(2, [a / (SR / 2), b / (SR / 2)], 'band', output='sos'), x)
def lp(x, f): return sosfilt(butter(2, f / (SR / 2), output='sos'), x)
def whoosh(d=0.45):
    n = int(d * SR); tt = np.arange(n) / SR
    x = rng.standard_normal(n); out = np.zeros(n)
    for i, f in enumerate(np.linspace(400, 3500, 8)):        # varredura de filtro
        seg = slice(i * n // 8, (i + 1) * n // 8)
        out[seg] = bp(x, f * 0.6, f * 1.4)[seg]
    env = np.sin(np.pi * tt / d) ** 2
    return out * env * 0.5, int(d * SR * 0.5)               # (som, amostra do pico)
def impacto(d=1.6):
    n = int(d * SR); tt = np.arange(n) / SR
    f = 60 * np.exp(-tt * 3) + 32
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 2.5)
    s += lp(rng.standard_normal(n), 300) * np.exp(-tt * 9) * 0.5
    return s * 0.8, 0
def subida(d=0.6):
    n = int(d * SR); tt = np.arange(n) / SR
    return bp(rng.standard_normal(n), 800, 7000) * (tt / d) ** 3 * 0.35, n
def flash(d=0.9):
    n = int(d * SR); tt = np.arange(n) / SR
    s = bp(rng.standard_normal(n), 2000, 9000) * np.exp(-tt * 7) * 0.35
    s += np.sin(2 * np.pi * 1200 * tt) * np.exp(-tt * 12) * 0.15
    return s, 0
def glitch(d=0.35):
    n = int(d * SR); s = np.zeros(n)
    for _ in range(14):
        a = int(rng.integers(0, n - 800)); l = int(rng.integers(300, 2500))
        f = rng.uniform(200, 4000); tt = np.arange(min(l, n - a)) / SR
        s[a:a + len(tt)] += np.sign(np.sin(2 * np.pi * f * tt)) * 0.18
    return lp(s, 6000), int(0.08 * SR)
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--parte', action='append', required=True)
    ap.add_argument('--duracao', type=float, required=True)
    ap.add_argument('--saida', required=True)
    a = ap.parse_args()
    N = int(a.duracao * SR); out = np.zeros(N)
    def put(sig, pico, t):
        i = int(t * SR) - pico
        if i < 0: sig = sig[-i:]; i = 0
        j = min(N, i + len(sig)); out[i:j] += sig[:j - i]
    for p in a.parte:
        arq, off = p.rsplit(':', 1)
        for tr in json.load(open(arq, encoding='utf-8')):
            t = float(off) + tr['t'] + 0.15      # entrada visual da cena
            tipo = tr['tipo']
            if tipo == 'whip': put(*whoosh(), t)
            elif tipo == 'zoom': put(*subida(), t); put(*impacto(), t)
            elif tipo == 'flash': put(*flash(), t); put(*impacto(1.0), t)
            elif tipo == 'glitch': put(*glitch(), t)
            elif tipo == 'corte': put(*impacto(0.8), t)
    out = np.tanh(out * 1.2)
    st = np.stack([out, out], 1)
    with wave.open(a.saida, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((st * 0.9 * 32767).astype(np.int16).tobytes())
    print('Pronto:', a.saida)
if __name__ == '__main__':
    main()
