#!/bin/bash
# Junta as partes, coloca voz + sons das transições + efeitos das animações + trilha, e masteriza.
# Uso: EP=pasta_do_episodio NOME="Título do vídeo - Canal.mp4" TRILHA=trilha.wav FX=fx.wav ./montar.sh
#   TRILHA e FX são opcionais (gerados pelo trilha/exemplo_trilha.py). Sem TRILHA, sai só com voz + sons.
set -e
AQUI="$(cd "$(dirname "$0")/.." && pwd)"
EP="${EP:?defina EP}"; NOME="${NOME:?defina NOME}"; TRILHA="${TRILHA:-}"; FX="${FX:-}"
cd "$EP"
N=$(ls *-ritmo.mp3 | wc -l)
: > lista.txt; for p in $(seq 1 $N); do echo "file 'parte$p.mp4'" >> lista.txt; done
# o reencode deixa o arquivo final bem menor (o fundo em movimento gera partes enormes)
ffmpeg -y -loglevel error -f concat -safe 0 -i lista.txt -c:v libx264 -preset faster -crf 21 -maxrate 7M -bufsize 14M -pix_fmt yuv420p video.mp4
ENT=""; for p in $(seq 1 $N); do ENT="$ENT -i $p-ritmo.mp3"; done
ffmpeg -y -loglevel error $ENT -filter_complex "concat=n=$N:v=0:a=1,aformat=sample_rates=48000:channel_layouts=stereo[a]" -map "[a]" voz.wav
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 voz.wav)
PARTES=""; for p in $(seq 1 $N); do OFF=$(python3 -c "import json;print(json.load(open('tempos.json'))['$p']['off'])"); PARTES="$PARTES --parte $p-ritmo.transicoes.json:$OFF"; done
python3 "$AQUI/sfx_transicoes.py" $PARTES --duracao $D --saida sfx.wav
if [ -n "$FX" ]; then
  ffmpeg -y -loglevel error -i voz.wav -i sfx.wav -i "$FX" -filter_complex \
    "[1:a]volume=-9dB[s];[2:a]aformat=sample_rates=48000:channel_layouts=stereo,alimiter=limit=0.16:attack=3:release=100:level=disabled[f];[0:a][s][f]amix=inputs=3:normalize=0:duration=first[a]" -map "[a]" voz_sfx.wav
else
  ffmpeg -y -loglevel error -i voz.wav -i sfx.wav -filter_complex "[1:a]volume=-9dB[s];[0:a][s]amix=inputs=2:normalize=0:duration=first[a]" -map "[a]" voz_sfx.wav
fi
ffmpeg -y -loglevel error -i video.mp4 -i voz_sfx.wav -map 0:v -map 1:a -c:v copy -c:a pcm_s16le -shortest com_voz.mov
if [ -n "$TRILHA" ]; then
  python3 "$AQUI/mixar_musica.py" --video com_voz.mov --trilha "$TRILHA:0:fim" --voz-tv --volume -14 --teto-trilha -21 --ducking 2.5 --lufs -13 --saida "$NOME"
else
  ffmpeg -y -loglevel error -i com_voz.mov -c:v copy -af loudnorm=I=-14:TP=-1.5 -c:a aac -b:a 192k "$NOME"
fi
echo "pronto: $NOME ($D s)"
ffmpeg -hide_banner -i "$NOME" -af ebur128 -f null - 2>&1 | grep -A3 Summary | grep "I:"
