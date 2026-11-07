# Instruções para o Claude

Você está num kit para produzir vídeos narrados de YouTube. O método está em `guias/`, as ferramentas em `motor/`, e **tudo o que é específico do canal está em `canal/`**. Leia isto inteiro antes de começar.

## 0. Primeiro contato: o perfil do canal

Abra `canal/PERFIL-DO-CANAL.md`.
- **Se ainda estiver com os campos `___`:** não produza nada. Entreviste a pessoa (no máximo 4 perguntas por vez) e preencha o perfil: nicho, público, narrador, tom, linhas editoriais, estilo visual, cores/fontes, voz, proibições. Use `exemplo/codex-obscuro/PERFIL-DO-CANAL.md` como referência de nível de detalhe. Ofereça valores padrão quando a pessoa não souber.
- **Se já estiver preenchido:** ele manda. Quando um guia e o perfil discordarem, vale o perfil (o guia é o padrão; o perfil é a escolha do canal).
- Leia também `canal/REGISTRO-DE-VIDEOS.md`: as lições dos vídeos anteriores valem mais que qualquer regra geral.

## 1. O pipeline (com portões)

Cada etapa só começa depois que a anterior foi aprovada pela pessoa nos pontos marcados com 🔒.

| # | Etapa | Guia | Saída | |
| --- | --- | --- | --- | --- |
| 1 | Pauta | `guias/01-ideia-e-pauta.md` | 3 a 5 ideias filtradas | 🔒 escolher |
| 2 | Embalagem | `guias/02-embalagem.md` | folha de aplicação: entrega, gatilhos, títulos A/B/C, esboço de thumb | 🔒 aprovar |
| 3 | Ficha da história | `guias/03-storytelling.md` | ficha preenchida | |
| 4 | Roteiro | `guias/04-roteiro-e-ritmo.md` + `modelos/roteiro.md` | roteiro com mapa visual (REAL/IA/ANIM) e fontes | 🔒 aprovar |
| 5 | Voz | `guias/06-voz.md` | `voz/parteN.txt` → `N.mp3` | 🔒 amostra da parte 1 |
| 6 | Imagens | `guias/05-imagens.md` | imagens reais com CREDITOS.md, lista de prompts de IA para a pessoa gerar | 🔒 a pessoa gera as de IA |
| 7 | Edição | `guias/07-edicao-motor.md` | alinhamento, ritmo, storyboards, animações, render | QA de quadros |
| 8 | Som | `guias/08-som-e-mix.md` | trilha + efeitos + mix a -13 LUFS | |
| 9 | Publicação | `guias/09-publicacao.md` | título, descrição com capítulos e créditos, tags, thumbs A/B | |
| 10 | Análise | `guias/10-analise.md` | linha no registro + 1 melhoria para o próximo | |

Trabalho que dá para refazer barato (ex.: um storyboard) não precisa de portão: faça e mostre.

## 2. Regras que não se negociam

1. **Embalagem antes do roteiro.** Se não sair um título e uma thumb fortes, a ideia não é produzida.
2. **Tudo que é afirmado como fato tem fonte.** Tabela de fontes no fim do roteiro. Número de "esforço" ("reuni 9 textos") é sempre verdadeiro.
3. **Imagens reais só com licença livre para uso comercial:** domínio público, CC0, CC BY, CC BY-SA — com crédito. Nunca NC, ND, agência de notícias ou "achei no Google". Use `motor/imagens/commons.py`.
4. **Chaves de API nunca aparecem** em mensagens, arquivos versionados ou logs. Leia do ambiente (`GEMINI_API_KEYS` / `GEMINI_KEYS_FILE`).
5. **Os 5 primeiros segundos funcionam sem som**, a cena 1 é a thumb em movimento, a frase 1 ecoa o título.
6. **Nenhuma tela parada por mais de 5 s.**
7. **Pessoas reais e povos reais com respeito:** o lado chocante de uma história é contado com prova e contexto, sem desumanizar ninguém e sem gore gratuito.
8. **Uma melhoria por vídeo**, anotada no registro.

## 3. Onde as coisas ficam (um episódio)

```
episodios/<slug>/
  roteiro-<slug>.md          narracao-<slug>.md (## Parte N, trechos separados por <break>)
  voz/estilo.txt  voz/parteN.txt  →  N.mp3, N-ritmo.mp3, *.alinhamento.json, tempos.json
  imagens-reais/ (+ CREDITOS.md)   imagens/ (doc-*.png, ia-*.png)   videos/ (anim-*.mp4, clip-*.mp4)
  storyboard-parteN.txt      tensao.json   trilha.wav  fx.wav
  thumb/   publicacao-<slug>.md
```

## 4. Como trabalhar

- Mostre rascunhos cedo (amostra de voz, 3 quadros do storyboard, esboço da thumb).
- Confira o próprio trabalho: ouça a duração da voz (≈0,29–0,37 s por palavra; muito acima = leu algo a mais), gere quadros de QA (`codex_motion.py quadros`), meça o LUFS final.
- Leia `guias/11-armadilhas-tecnicas.md` antes de rodar renders longos.
- Ao terminar, peça os números do vídeo depois de 48 h e 7 dias.
