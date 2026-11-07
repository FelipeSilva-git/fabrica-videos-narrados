# 07 · Edição: o motor

O motor (`motor/motion.py`) transforma **áudio + texto + storyboard** em vídeo 1080p/30 fps com fundo animado, imagens, animações, números, transições e chamadas.

## Ordem
```bash
EP=episodios/meu-ep; MD=$EP/narracao-meu-ep.md
python3 motor/scripts/alinhar_partes.py $EP $MD                 # 1. onde cada trecho começa/termina
# 2. escreva plano.json com as pausas (ver guia 04 / ritmo.py)
python3 motor/scripts/ritmo.py $EP $EP/plano.json               # 3. N-ritmo.mp3
python3 motor/scripts/alinhar_partes.py $EP $MD -ritmo          # 4. realinha
python3 motor/scripts/linha_do_tempo.py $EP                     # 5. tempos.json (offsets das partes)
python3 motor/motion.py storyboard --texto $MD --parte 1 --saida $EP/storyboard-parte1.txt   # 6. em branco
# 7. preencha os storyboards; faça as animações (abaixo); confira quadros:
python3 motor/motion.py quadros --audio $EP/1-ritmo.mp3 --texto $MD --parte 1 --storyboard $EP/storyboard-parte1.txt --imagens $EP --tempos 2,10,25 --saida $EP/quadros
EP=$EP MD=$MD DESTAQUE=ambar CHAMADA="2:40" motor/scripts/render_partes.sh 1 2 3 4 5 6   # 8. render
```

## Comandos do storyboard
Cada `[NN]` é um trecho da narração (separado por `<break>`). As linhas abaixo dele dizem o que aparece.

| Comando | O que faz |
| --- | --- |
| `documento: imagens/doc-r01.png` | **Imagem real** em cor, como documento (papel + sombra + selo). Não vira line-art |
| `imagem: imagens/ia-03.png` | Imagem line-art (PNG transparente ou JPG de fundo preto) |
| `video: videos/anim-01.mp4` | Clipe/animação; substitui a imagem da cena |
| `efeito: zoom` / `desenhar` / `deslizar` | Como a imagem entra |
| `transicao: corte` / `whip` / `zoom` / `flash` / `glitch` | Como a cena **entra**, com som próprio (padrão: fusão) |
| `+ palavra` | **Sub-cena:** troca o visual quando "palavra" é falada (`+` sozinho divide o tempo) |
| `texto: frase com *destaque*` | Frase na tela (evite: prefira animação) |
| `falado` | Escreve o que está sendo dito, palavra por palavra |
| `numero: 6.700 m \| altitude` | Contador que sobe até o número |
| `titulo: I \| subtítulo` | Cartão de capítulo |
| `legenda:` / `fonte:` | Texto pequeno embaixo / crédito no canto |
| `print: prints/x.png` | Print num cartão inclinado |
| `selo: 0.6` | Brilho do selo fixo do canto (com `--selo imagem.png`) |
| `manter` | Continua a cena anterior |
| `preto` | Só o fundo (**não** combine com `texto`: some o texto) |

Exemplo:
```
[02] Ela foi encontrada no topo de um vulcão...
documento: imagens/doc-r06.png
efeito: zoom
+ onde quase nada vive
documento: imagens/doc-r08.png
efeito: zoom

[06] Março de mil novecentos e noventa e nove...
video: videos/anim-cap1.mp4
transicao: flash
```

## Transições: só com motivo
| Transição | Quando |
| --- | --- |
| fusão (padrão) | explicação calma |
| `whip` | listas e montagens |
| `corte` | **depois de frase de impacto** (o mais aprovado) |
| `zoom` | revelação, número forte |
| `flash` | grande revelação, abertura de capítulo |
| `glitch` | algo "errado", terror |
No máximo **uma transição forte a cada 10–15 s**; variar os tipos.

## Opções do render
`--destaque vermelho|ambar|azul|#RRGGBB` (cor do canal, no perfil) · `--chamadas 40` (like/inscreva-se aos 40 s da parte; 2 por vídeo: ~2:00 e antes da reflexão final) · `--fade-final` · `--tensao tensao.json --tensao-offset <off>` (o fundo se mexe com a curva de tensão do vídeo inteiro: `[[t, 0..1], ...]`) · `--res 720` e `--de/--ate` para prévias · `--sem-audio` (o áudio entra na montagem).

## Animações (palitos em código)
`motor/animacao/`: `base.py` (desenho com cairo: `humano`, `anjo`, `livro_aberto`, `corrente`, `casa`, `montanha`, `estrela`, `nuvem`, poses, câmera, `render`, `quadros`, `folha`), `extras.py` (chapéu, chama, faísca, `principal`), `helpers.py` (seta, arco, navio, onda, oca, arco e flecha, clava, fogueira, rótulos).
- Copie `exemplo_animacoes.py`: cada animação é `(função de cena, duração, nome, textos)`.
- `python3 exemplo_animacoes.py teste <nome> 1.0,2.5` gera quadros soltos para conferir; `render <nome|todos>` gera os MP4.
- **Faça já sabendo a duração da cena** (tempos.json) e **em que segundo cada som acontece** (para o fx.wav).
- Rótulos grandes só na fase deles (não sobrepor). Use "-" ASCII (a fonte não tem o "−").
- Capítulos: `cartoes_capitulo.py` (numeral romano + ícone).

## QA antes de entregar
- Folha de quadros de cada parte (`quadros` + `folha`): nada cortado, nada sobreposto, crédito legível.
- Nenhuma tela parada > 5 s; 5 primeiros segundos entendíveis sem som.
