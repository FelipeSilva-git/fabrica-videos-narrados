"""Acrescenta silêncio de propósito depois de trechos escolhidos (frases de impacto, viradas de bloco).
O corte é feito no ponto mais silencioso entre os dois trechos, então não corta palavra.

Uso: python3 ritmo.py <pasta_episodio> plano.json
plano.json: {"1": {"pausas": {"3": 0.8, "5": 1.0}, "cauda": 0.6}, "2": {...}, ...}
  -> na parte 1, +0,8 s depois do trecho 3, +1,0 s depois do 5, e 0,6 s de silêncio no fim.
Precisa de N.mp3 e N.alinhamento.json (rode alinhar_partes.py antes). Saída: N-ritmo.mp3.
Depois rode alinhar_partes.py de novo com o sufixo -ritmo.

Valores que funcionaram: 0,4–0,6 s entre ideias; 0,8–1,0 s depois de frase de impacto;
1,0–1,5 s antes de um capítulo novo; 3,5 s de cauda na última parte (tela final).
"""
import json, subprocess, sys, os
import numpy as np
SR = 48000
pasta, plano = sys.argv[1], json.load(open(sys.argv[2]))
for p, cfg in plano.items():
    ins = {int(k): float(v) for k, v in cfg.get('pausas', {}).items()}; cauda = float(cfg.get('cauda', 0.6))
    tr = json.load(open(os.path.join(pasta, f'{p}.alinhamento.json'), encoding='utf-8'))['trechos']
    x = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', os.path.join(pasta, f'{p}.mp3'), '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'],
                                     capture_output=True).stdout, np.float32)
    ped, ult = [], 0
    for k in sorted(ins):
        a, b = tr[k - 1]['fim'], tr[k]['inicio']
        i0, i1 = int(a * SR), int(b * SR)
        seg = np.abs(x[i0:i1]); win = 2400
        en = np.convolve(seg, np.ones(win) / win, 'same') if len(seg) > win else seg
        m = i0 + int(np.argmin(en)) if len(en) else (i0 + i1) // 2
        ped += [x[ult:m], np.zeros(int(ins[k] * SR), np.float32)]; ult = m
    ped += [x[ult:], np.zeros(int(cauda * SR), np.float32)]
    y = np.concatenate(ped)
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-', '-c:a', 'libmp3lame', '-b:a', '192k',
                    os.path.join(pasta, f'{p}-ritmo.mp3')], input=y.tobytes(), check=True)
    print('parte', p, round(len(x) / SR, 2), '->', round(len(y) / SR, 3))
