"""Monta a linha do tempo do vídeo inteiro a partir das partes (N-ritmo.mp3 + alinhamento).

Uso: python3 linha_do_tempo.py <pasta_episodio>
Saída: <pasta>/tempos.json  {"1": {"off": 0, "dur": ..., "tr": [[ini, fim], ...]}, ..., "FIM": total}
Use os "off" como --tensao-offset no render e nas emendas da montagem, e para os capítulos da descrição.
"""
import json, subprocess, sys, os, glob
pasta = sys.argv[1]
partes = sorted(int(os.path.basename(f).split('-')[0]) for f in glob.glob(os.path.join(pasta, '*-ritmo.mp3')))
o = 0.0; TP = {}
for p in partes:
    a = os.path.join(pasta, f'{p}-ritmo.mp3')
    d = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', a], capture_output=True, text=True).stdout)
    tr = json.load(open(a[:-4] + '.alinhamento.json', encoding='utf-8'))['trechos']
    TP[str(p)] = {'off': round(o, 3), 'dur': d, 'tr': [[round(o + x['inicio'], 2), round(o + x['fim'], 2)] for x in tr]}
    o += d
TP['FIM'] = round(o, 3)
json.dump(TP, open(os.path.join(pasta, 'tempos.json'), 'w'))
for p in partes:
    off = TP[str(p)]['off']; print(f'parte {p}: começa em {off:8.3f} s  ({int(off // 60)}:{int(off % 60):02d})')
print(f'total: {o:.2f} s ({int(o // 60)}:{int(o % 60):02d})')
