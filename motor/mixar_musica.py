#!/usr/bin/env python3
"""
MIXAR MÚSICA — coloca trilha de fundo embaixo da narração.

- Cada trecho de música: --trilha "arquivo.mp3:INICIO:FIM[:OFFSET]"  (segundos no vídeo; OFFSET = de onde a música começa)
- Trechos vizinhos se cruzam com fade (--cruzar segundos).
- A música abaixa sozinha quando o narrador fala (ducking) e o volume final fica no padrão do YouTube (-14 LUFS).

  python3 mixar_musica.py --video video_com_voz.mp4 \
      --trilha "quente.mp3:0:126" --trilha "fria.mp3:126:330" --trilha "quente.mp3:330:fim:55" \
      --saida final.mp4
"""
import argparse, subprocess

def duracao(f):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f],
                       capture_output=True, text=True)
    return float(r.stdout.strip())

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--video', required=True)
    ap.add_argument('--trilha', action='append', required=True)
    ap.add_argument('--saida', required=True)
    ap.add_argument('--volume', type=float, default=-27.0, help='volume da música em dB (antes do ducking). Padrão aprovado no canal: -27')
    ap.add_argument('--cruzar', type=float, default=3.0)
    ap.add_argument('--fade-final', type=float, default=2.5)
    ap.add_argument('--voz-tv', action='store_true', help='voz mais presente: EQ (corta grave sobrando, realça 3 kHz) + compressão leve. Pensado para TV')
    ap.add_argument('--ducking', type=float, default=6.0, help='quanto a música abaixa quando a voz entra (razão do compressor). 6 = abaixa muito; 2,5 = a música continua presente')
    ap.add_argument('--lufs', type=float, default=-14.0)
    ap.add_argument('--teto-trilha', type=float, default=None, help='teto de pico da trilha em dBFS depois do volume (ex.: -22). Corta os picos que passam a voz')
    a = ap.parse_args()

    total = duracao(a.video)
    cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-i', a.video]
    filtros, rotulos = [], []
    for i, t in enumerate(a.trilha):
        partes = t.split(':')
        arq, ini, fim = partes[0], float(partes[1]), partes[2]
        fim = total if fim == 'fim' else float(fim)
        off = float(partes[3]) if len(partes) > 3 else 0.0
        c = a.cruzar
        ini_r = max(0.0, ini - (c if i > 0 else 0))
        fim_r = min(total, fim + (c if fim < total else 0))
        dur = fim_r - ini_r
        cmd += ['-i', arq]
        k = i + 1
        dmus = duracao(arq)
        # se o trecho for maior que a música, emenda a música nela mesma com fade cruzado
        if off + dur > dmus - 1:
            filtros.append(f'[{k}:a]asplit[m{k}a][m{k}b];[m{k}a][m{k}b]acrossfade=d=8[m{k}l]')
            fonte = f'[m{k}l]'
        else:
            fonte = f'[{k}:a]'
        fin = 2.0 if i == 0 else c
        fout = a.fade_final if fim_r >= total - 0.01 else c
        filtros.append(f'{fonte}atrim={off}:{off + dur},asetpts=PTS-STARTPTS,'
                       f'afade=t=in:st=0:d={fin},afade=t=out:st={max(0, dur - fout)}:d={fout},'
                       f'aformat=sample_rates=48000:channel_layouts=stereo,'
                       f'adelay={int(ini_r * 1000)}|{int(ini_r * 1000)}[t{i}]')
        rotulos.append(f'[t{i}]')
    filtros.append(f'{"".join(rotulos)}amix=inputs={len(rotulos)}:normalize=0:duration=longest,'
                   f'volume={a.volume}dB,' + (f'alimiter=limit={10 ** (a.teto_trilha / 20):.4f}:attack=5:release=120:level=disabled,' if a.teto_trilha is not None else '') + f'atrim=0:{total}[mus]')
    eq = ('highpass=f=70,equalizer=f=220:t=q:w=1.2:g=-2,equalizer=f=3200:t=q:w=1.0:g=4,'
          'equalizer=f=7000:t=q:w=1.5:g=1.5,acompressor=threshold=0.08:ratio=3:attack=8:release=180:makeup=2.5,') if a.voz_tv else ''
    filtros.append(f'[0:a]aformat=sample_rates=48000:channel_layouts=stereo,{eq}asplit[voz][chave]')
    # ducking: a voz comanda o compressor da música
    filtros.append(f'[mus][chave]sidechaincompress=threshold=0.03:ratio={a.ducking}:attack=40:release=600:makeup=1[musd]')
    filtros.append(f'[voz][musd]amix=inputs=2:normalize=0:duration=first,loudnorm=I={a.lufs}:TP=-1.2:LRA={7 if a.voz_tv else 11}[a]')
    cmd += ['-filter_complex', ';'.join(filtros), '-map', '0:v', '-map', '[a]',
            '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', a.saida]
    subprocess.run(cmd, check=True)
    print('Pronto:', a.saida)

if __name__ == '__main__':
    main()
