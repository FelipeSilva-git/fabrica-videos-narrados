#!/bin/bash
# Renderiza as partes de um episódio (sem áudio; o áudio entra na montagem).
# Uso: EP=pasta_do_episodio MD=narracao.md DESTAQUE=ambar CHAMADA="3:63.3" ./render_partes.sh 1 2 3 ...
#   CHAMADA="parte:segundo" -> em que parte/segundo entra o card de like/inscreva-se
#   Rode 2 cadeias em paralelo em máquinas com 2+ núcleos (ex.: "1 2 3" e "6 5 4").
set -u
AQUI="$(cd "$(dirname "$0")/.." && pwd)"
M="$AQUI/motion.py"
EP="${EP:?defina EP}"; MD="${MD:?defina MD}"; DESTAQUE="${DESTAQUE:-ambar}"; CHAMADA="${CHAMADA:-}"
ULT=$(ls "$EP"/*-ritmo.mp3 | wc -l)
for p in "$@"; do
  OFF=$(python3 -c "import json;print(json.load(open('$EP/tempos.json'))['$p']['off'])")
  extra=""
  [ -n "$CHAMADA" ] && [ "${CHAMADA%%:*}" = "$p" ] && extra="--chamadas ${CHAMADA#*:}"
  [ "$p" = "$ULT" ] && extra="$extra --fade-final"
  TENS=""; [ -f "$EP/tensao.json" ] && TENS="--tensao $EP/tensao.json --tensao-offset $OFF"
  python3 "$M" render --audio "$EP/$p-ritmo.mp3" --texto "$MD" --parte $p --storyboard "$EP/storyboard-parte$p.txt" \
    --imagens "$EP" --destaque "$DESTAQUE" --sem-audio $TENS $extra --saida "$EP/parte$p.mp4" > "$EP/render$p.log" 2>&1
  echo "parte $p $(date +%T) saída=$?" >> "$EP/render.log"
done
