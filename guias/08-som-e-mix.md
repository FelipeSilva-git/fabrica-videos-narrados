# 08 · Som e mix

Quatro camadas: **voz** · **sons das transições** (`sfx_transicoes.py`, automático) · **efeitos das animações** (`fx.wav`) · **trilha** (`trilha.wav`).

## Trilha própria (sem direitos autorais)
`motor/trilha/exemplo_trilha.py` sintetiza a música em código (instrumentos em `motor/sfx_lib.py`: `pad`, `pluck`, `ney`, `coro`, `sino`, `tambor`, `taiko`, `coracao`, `impacto`, `subida`, `whoosh`, `fogo`, `vento`, `multidao`, `agua`, `pagina`, `rachar`…).
```bash
python3 motor/trilha/exemplo_trilha.py episodios/ep episodios/ep    # lê tempos.json -> trilha.wav + fx.wav
```
Copie e adapte por episódio:
- **Clima por bloco** definido no roteiro (calmo, tensão, susto, revelação, silêncio).
- **Cama do tema:** um som "do mundo" do episódio (vento na montanha, mar, floresta).
- **Antes da transição forte, cresce** (1–3 s); **depois, drop** ou troca de textura.
- **Acompanha a fala:** pulso leve em listas; quase só grave em frase de impacto.
- **Contínua do começo ao fim**; silêncio só nos buracos de 1–2 s depois de frases de impacto e antes da maior revelação.
- **Todo efeito de animação** (fogo, passos, vento, multidão, páginas) vai no `fx.wav`, no segundo certo.
- Fechamento resolve (acorde maior/calmo).

Alternativa: música de gerador (Suno etc.) instrumental, 2–3 versões, a mais calma e constante; mix com `--volume -27`.

## Mix padrão (aprovado)
```bash
EP=episodios/ep NOME="Título - Canal.mp4" TRILHA=trilha.wav FX=fx.wav motor/scripts/montar.sh
```
Por dentro:
- Sons de transição a **-9 dB**.
- `fx.wav` com teto de pico `alimiter limit=0.16` (nenhum efeito passa a voz).
- `mixar_musica.py --voz-tv --volume -14 --teto-trilha -21 --ducking 2.5 --lufs -13`
  - `--voz-tv`: tira grave sobrando, +3 kHz, compressão leve (entende-se na TV; quase metade do tempo assistido pode ser na TV).
  - trilha alta e contínua, mas com teto: nenhum impacto passa a voz.
- Final em **-13 LUFS** integrado. Confira com `ffmpeg -i final.mp4 -af ebur128 -f null -`.

## Conferir
- Ouça 3 trechos: gancho, um impacto, o fim.
- A voz sempre por cima; nada de clipping; o fim não corta seco.
