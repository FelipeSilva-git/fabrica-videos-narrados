"""Narração com o Google AI Studio (Gemini TTS).
Chaves (nunca coloque no repositório): variável GEMINI_API_KEYS="chave1,chave2" ou um arquivo
fora do repositório indicado em GEMINI_KEYS_FILE (aceita curinga, ex.: ~/Downloads/googlestudio_api*.txt). Troca de chave quando a cota acaba.
Uso: python3 google_tts.py texto.txt saida.wav [--voz Umbriel] [--estilo "..."]
"""
import json, re, sys, os, base64, glob, wave, urllib.request, urllib.error, argparse
def chaves():
    ks = [k.strip() for k in os.environ.get('GEMINI_API_KEYS', '').split(',') if k.strip()]
    arq = os.environ.get('GEMINI_KEYS_FILE', '')
    for f in sorted(glob.glob(os.path.expanduser(arq))) if arq else []:
        if os.path.exists(f):
            t = open(f, encoding='utf-8', errors='ignore').read()
            ks += re.findall(r'AIza[0-9A-Za-z_\-]{30,}|AQ\.[0-9A-Za-z_\-\.]{20,}', t)
    if not ks:
        raise SystemExit('Nenhuma chave: defina GEMINI_API_KEYS ou GEMINI_KEYS_FILE.')
    return list(dict.fromkeys(ks))
def chamar(url, corpo, k):
    req = urllib.request.Request(url, data=json.dumps(corpo).encode() if corpo else None,
        headers={'Content-Type': 'application/json', 'x-goog-api-key': k})
    with urllib.request.urlopen(req, timeout=170) as r:
        return json.loads(r.read())
def modelos(k):
    d = chamar('https://generativelanguage.googleapis.com/v1beta/models?pageSize=200', None, k)
    return [m['name'] for m in d.get('models', []) if 'tts' in m['name']]
def gerar(texto, voz, estilo, modelo):
    corpo = {'contents': [{'parts': [{'text': (estilo + '\n\n#### TRANSCRIPT\n' + texto) if estilo else texto}]}],
             'generationConfig': {'responseModalities': ['AUDIO'],
                 'speechConfig': {'voiceConfig': {'prebuiltVoiceConfig': {'voiceName': voz}}}}}
    erro = None
    for i, k in enumerate(chaves()):
        try:
            d = chamar(f'https://generativelanguage.googleapis.com/v1beta/{modelo}:generateContent', corpo, k)
            p = d['candidates'][0]['content']['parts'][0]['inlineData']
            return base64.b64decode(p['data']), p.get('mimeType', '')
        except urllib.error.HTTPError as e:
            erro = f'chave {i+1}: HTTP {e.code} {e.read()[:300]!r}'
            print(erro, file=sys.stderr)
    raise SystemExit('todas as chaves falharam: ' + str(erro))
if __name__ == '__main__':
    a = argparse.ArgumentParser()
    a.add_argument('texto', nargs='?'); a.add_argument('saida', nargs='?')
    a.add_argument('--voz', default='Umbriel'); a.add_argument('--estilo', default='')
    a.add_argument('--modelo', default='models/gemini-3.8-flash-tts')
    a.add_argument('--listar', action='store_true')
    o = a.parse_args()
    if o.listar:
        print(len(chaves()), 'chaves');
        for k in chaves():
            try: print(modelos(k)); break
            except urllib.error.HTTPError as e: print('HTTP', e.code)
        sys.exit()
    pcm, mime = gerar(open(o.texto, encoding='utf-8').read(), o.voz, o.estilo, o.modelo)
    if pcm[:4] == b'RIFF':
        open(o.saida, 'wb').write(pcm)
        with wave.open(o.saida) as w: print('ok', o.saida, round(w.getnframes() / w.getframerate(), 2), 's', mime)
        sys.exit()
    rate = int(re.search(r'rate=(\d+)', mime).group(1)) if 'rate=' in mime else 24000
    with wave.open(o.saida, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate); w.writeframes(pcm)
    print('ok', o.saida, round(len(pcm) / 2 / rate, 2), 's', mime)
