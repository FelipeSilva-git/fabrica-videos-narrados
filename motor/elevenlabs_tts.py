"""Narração com o ElevenLabs (alternativa ao Gemini TTS).
Chave (nunca no repositório): variável ELEVENLABS_API_KEY.
Uso:
  python3 elevenlabs_tts.py --listar                                   # vozes da sua conta (nome e id)
  python3 elevenlabs_tts.py texto.txt saida.mp3 --voz <voice_id> [--modelo eleven_multilingual_v2]
No ElevenLabs as pausas podem ir no texto: <break time="1.0s" /> (até 3 s). Números por extenso.
Textos longos: divida em partes de até ~4.500 caracteres (uma parte por arquivo).
"""
import os, sys, json, argparse, urllib.request, urllib.error

def chave():
    k = os.environ.get('ELEVENLABS_API_KEY', '').strip()
    if not k:
        raise SystemExit('Defina ELEVENLABS_API_KEY (crie em elevenlabs.io > Profile > API Keys).')
    return k

def pedir(url, corpo=None):
    req = urllib.request.Request(url, data=json.dumps(corpo).encode() if corpo else None,
                                 headers={'xi-api-key': chave(), 'Content-Type': 'application/json', 'Accept': 'audio/mpeg' if corpo else 'application/json'})
    try:
        return urllib.request.urlopen(req, timeout=300).read()
    except urllib.error.HTTPError as e:
        raise SystemExit(f'ElevenLabs respondeu {e.code}: {e.read()[:300]!r}')

if __name__ == '__main__':
    a = argparse.ArgumentParser()
    a.add_argument('texto', nargs='?'); a.add_argument('saida', nargs='?')
    a.add_argument('--voz', default=''); a.add_argument('--modelo', default='eleven_multilingual_v2')
    a.add_argument('--estabilidade', type=float, default=0.5); a.add_argument('--similaridade', type=float, default=0.75)
    a.add_argument('--listar', action='store_true')
    o = a.parse_args()
    if o.listar:
        for v in json.loads(pedir('https://api.elevenlabs.io/v1/voices'))['voices']:
            print(v['voice_id'], '|', v['name'], '|', v.get('labels', {}))
        sys.exit()
    if not (o.texto and o.saida and o.voz):
        a.error('informe texto, saída e --voz')
    txt = open(o.texto, encoding='utf-8').read().strip()
    mp3 = pedir(f'https://api.elevenlabs.io/v1/text-to-speech/{o.voz}?output_format=mp3_44100_192',
                {'text': txt, 'model_id': o.modelo, 'voice_settings': {'stability': o.estabilidade, 'similarity_boost': o.similaridade}})
    open(o.saida, 'wb').write(mp3)
    print('ok', o.saida, len(mp3) // 1024, 'KB', len(txt.split()), 'palavras')
