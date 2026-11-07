"""Alinha cada parte da narração com o texto (onde começa e termina cada trecho).

Uso: python3 alinhar_partes.py <pasta_episodio> <narracao.md> [sufixo]
  - áudios: <pasta>/1.mp3, 2.mp3 ... (ou 1-ritmo.mp3 com sufixo "-ritmo")
  - narracao.md: seções "## Parte N", trechos separados por <break time="1.0s" />
Saída: <pasta>/N[sufixo].alinhamento.json, e uma lista dos trechos com os tempos e a pausa até o próximo.
"""
import sys, os, json, hashlib, glob
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from codex_motion import texto_da_parte
from alinhar import alinhar

pasta, md = sys.argv[1], sys.argv[2]
suf = sys.argv[3] if len(sys.argv) > 3 else ''
partes = sorted(int(os.path.basename(f).split('.')[0]) for f in glob.glob(os.path.join(pasta, '[0-9].mp3')) + glob.glob(os.path.join(pasta, '[0-9][0-9].mp3')))
for p in partes:
    a = os.path.join(pasta, f'{p}{suf}.mp3')
    t = texto_da_parte(md, p)
    al = alinhar(a, t)
    al['chave'] = hashlib.md5((t + str(os.path.getsize(a))).encode()).hexdigest()
    json.dump(al, open(a[:-4] + '.alinhamento.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('PARTE', p, al.get('aviso', ''), al['duracao'])
    tr = al['trechos']
    for i, x in enumerate(tr, 1):
        gap = (tr[i]['inicio'] - x['fim']) if i < len(tr) else 0
        print(f"{i:02d} {x['inicio']:6.2f}-{x['fim']:6.2f} pausa {gap:4.2f}  {x['texto'][:60]}")
