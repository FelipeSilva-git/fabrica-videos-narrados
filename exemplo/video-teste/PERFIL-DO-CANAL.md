# Perfil do canal — Canal Teste

## 1. Identidade
- **Nome do canal:** Canal Teste
- **Idioma principal / outros idiomas:** português do Brasil · versões em inglês (thumb, descrição, legenda)
- **Nicho em uma frase:** histórias e culturas antigas pelo lado feio e obscuro (rituais, sacrifícios, costumes com os mortos), sempre com prova.
- **Tema do canal:** "o que foi escondido de você".
- **Promessa para quem se inscreve:** cada vídeo é uma página nova do arquivo, com a história que os livros de escola pularam — e a prova.

## 2. Público
- **Quem assiste:** homens e mulheres de 25 a 54, Brasil e Portugal, que gostam de mistério, terror real, Bíblia oculta, arqueologia.
- **Pontos de identificação:** "maldição da múmia", "sacrifício humano dos incas/astecas", "canibalismo dos índios" das aulas de história, filmes de terror.
- **Onde assiste:** celular e **TV** (até 46% do tempo) → voz equalizada para TV.

## 3. Narrador
- **Quem conta:** O Narrador.
- **Arco:** ele está montando um arquivo com o que foi apagado; cada vídeo é uma página, e o fechamento aponta a próxima.
- **Tom:** misterioso, investigativo, empático com as vítimas. Frases curtas.
- **Fala com:** "você", "ouvinte".
- **Marcas verbais:** "o lado obscuro de…", prisão/cela/sombra/luz.
- **Abertura opcional:** "Sente-se. Hoje eu vou te mostrar o lado obscuro de…" (só quando cabe no gancho).

## 4. Linhas editoriais
| Linha | Exemplos de pauta | Prova exigida | Playlist |
| --- | --- | --- | --- |
| Culturas antigas, o lado obscuro | capacocha inca, Hans Staden e os tupinambás, sacrifícios astecas, múmias | relato de testemunha, descoberta arqueológica, estudo publicado | "Culturas Antigas: o Lado Obscuro" |
| Bíblia oculta e textos proibidos | Enoque, Adão, gnósticos | o texto antigo, com fonte | "Bíblia Oculta" |
| Terror e mistério real | paralisia do sono, criaturas | estudos, relatos documentados | "Mistério Real" |

**Fora do foco:** fé e comportamento atual (o vídeo do bezerro de ouro teve poucas views), autoajuda, política.

## 5. Visual
- **Cor de destaque:** `ambar` (culturas antigas) · `vermelho` (tensão/terror)
- **Fundo:** textura hachurada escura com movimento lento + tensão (`--tensao`)
- **Fontes:** Cinzel (títulos), Cormorant Garamond (frases), Special Elite (créditos), Anton (thumbs)
- **Camadas:** REAL 60% · ANIM 25% · IA 15%
- **Selo das imagens reais:** "REGISTRO REAL", âmbar (255,180,64)
- **Prompt-base de IA:**
```
Minimalist white line art illustration on a solid pure black background. Clean white outlines of uniform thickness, no fill, no shading, no gray, no color, no text, no letters. Simple faceless human figures. Centered composition with generous empty black space around the subject. 16:9.
```
- **Animações:** palitos de traço branco, destaque âmbar, "SIMULAÇÃO" no canto quando reconstrói fato.
- **Thumb:** foto real mais marcante (rosto, descoberta) + elemento line-art com borda esfumada; texto Anton de 2–4 palavras com 1 palavra em cor; contradição > palavra solta.

## 6. Voz
- **Motor:** Gemini TTS · **modelo:** `models/gemini-3.8-flash-tts` · **voz:** Umbriel · **estilo:** Empathetic
- **Notas do diretor:** `episodio-menina-inca/voz/estilo.txt`

## 7. Som
- **Clima:** grave contínuo, pads frios, percussão andina/ritual por bloco, silêncio antes da grande revelação.
- **Texturas:** vento de montanha, fogo, tambores, coro distante.
- **Mix:** padrão (`--voz-tv --volume -14 --teto-trilha -21 --ducking 2.5 --lufs -13`).

## 8. Formato
- **Duração:** 9–11 min · **6 partes de voz** · 1 vídeo por semana
- **Chamada:** ~2:00 e antes da reflexão final, ligada ao próximo vídeo
- **Fechamento:** volta à imagem da abertura + pergunta + próxima página do arquivo
- **Short-isca:** sim

## 9. Regras e proibições
- Povos e pessoas reais com respeito: o lado obscuro é contado com contexto e prova, nunca como "selvagens". Restos humanos sem close gratuito.
- Sem gore; IA com pessoas sem rosto.
- Política: criticar o sistema, nunca um lado; não chamar o público de "gado".
- Imagens reais: só PD, CC0, CC BY, CC BY-SA, com crédito.
