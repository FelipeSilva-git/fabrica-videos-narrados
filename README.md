# Fábrica de Vídeos Narrados

Um kit para produzir **vídeos longos de YouTube narrados** (documentário, história, mistério, ciência, curiosidades) com **Claude**: da ideia ao vídeo final masterizado, com roteiro, voz, imagens reais com licença, animações em código, trilha própria e textos de publicação.

Ele nasceu no canal **Códex Obscuro** (histórias antigas pelo lado obscuro) e foi separado em duas camadas para servir a **qualquer canal**:

| Camada | O que é | Muda de canal para canal? |
| --- | --- | --- |
| `guias/` + `motor/` | Método (embalagem, storytelling, roteiro, ritmo, som) e ferramentas | Não |
| `canal/` | Perfil do canal: nicho, público, narrador, tom, cores, fontes, voz, proibições, registro de resultados | **Sim**: é o único lugar que precisa ser preenchido |

`exemplo/codex-obscuro/` mostra um canal real preenchido e um episódio completo.

## Como usar com o Claude

1. Clone o repositório e abra a pasta numa conversa com o Claude (Claude Code, ou envie a pasta).
2. Diga: **"leia o CLAUDE.md e vamos montar o perfil do meu canal"**. O Claude faz as perguntas e preenche `canal/PERFIL-DO-CANAL.md`.
3. Depois: **"vamos fazer um vídeo sobre ___"**. O Claude segue o pipeline com portões de aprovação (embalagem → ficha → roteiro → voz → imagens → render → mix → publicação).
4. Depois de publicar, mande os números do YouTube Studio. O Claude preenche `canal/REGISTRO-DE-VIDEOS.md` e escolhe **uma melhoria** para o próximo.

Também dá para instalar as skills de `skills/` (formato SKILL.md) para o Claude carregar o método sozinho.

## O pipeline

```
ideia → EMBALAGEM (título + thumb antes de tudo) → ficha da história → roteiro com mapa visual
      → voz (Gemini TTS) → alinhamento → ritmo (pausas) → storyboard → imagens reais / IA / animações
      → render por partes → montagem + sons + trilha → mix (-13 LUFS) → QA → publicação → análise
```

Cada etapa tem um guia em `guias/` e um modelo em `modelos/`.

## Requisitos

- Python 3.10+, `ffmpeg` no PATH
- `pip install numpy pillow opencv-python-headless pycairo`
- Voz: chave do Google AI Studio (Gemini TTS) em `GEMINI_API_KEYS` (vírgulas) ou num arquivo apontado por `GEMINI_KEYS_FILE`. **Nunca coloque chaves no repositório** (o `.gitignore` já bloqueia os nomes comuns).
- Imagens de IA: qualquer gerador (Flow, Midjourney…) gerado por você; o kit dá os prompts.

## Estrutura

```
CLAUDE.md                 ← instruções para o Claude (comece por aqui)
canal/                    ← PERFIL, REGISTRO de resultados, PAUTAS (preencher por canal)
guias/01..11              ← o método, etapa por etapa
modelos/                  ← modelos em branco (roteiro, storyboard, narração, publicação...)
motor/                    ← código: motor de motion, voz, alinhamento, mix, sons, trilha, animações
skills/                   ← skills prontas para o Claude
exemplo/codex-obscuro/    ← um canal real preenchido + episódio completo
```

## Licença

Código e textos: MIT (veja `LICENSE`). Fontes em `motor/fontes/`: OFL/Apache (veja `motor/fontes/LICENCAS.md`).

---

### English summary

A Claude-driven kit for producing long-form **narrated YouTube videos** end to end: packaging (title + thumbnail first), story structure, scripting with retention rules, Gemini TTS voice, forced alignment, pacing, a Python motion engine (storyboard → MP4), licensed real images from Wikimedia Commons with automatic credits, code-drawn stick-figure animations, a synthesized soundtrack, mixing to -13 LUFS and publishing copy. Everything channel-specific lives in `canal/PERFIL-DO-CANAL.md`; tell Claude to read `CLAUDE.md` and it will interview you to fill it in. Docs are in Portuguese.
