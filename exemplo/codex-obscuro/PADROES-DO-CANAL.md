# CÓDEX OBSCURO — Padrões do canal

Tudo o que já foi aprovado nos vídeos *O Favorzinho* e *Até a luz de antigamente era diferente*.
Use este arquivo como ponto de partida de cada episódio novo.

---

## 1. Identidade

- **Narrador:** O Velho Contador. Voz masculina, grave, rouca e lenta (ElevenLabs).
- **Voz (a partir do Staden, nov/2026):** Google AI Studio (Gemini TTS, `gemini-3.8-flash-tts`), voz **Umbriel**, estilo **Empathetic**. Gerar com `codex-motion/google_tts.py` (lê as chaves em `Downloads/googlestudio_api*.txt` e troca de chave quando a cota acaba). O estilo vai separado como "notas do diretor" (`staden/voz/estilo.txt`) e o texto depois de `#### TRANSCRIPT`; senão a voz lê as instruções. Sem tags `<break>`: as pausas vêm dos parágrafos.
- **Tom:** misterioso e investigativo, falando com "você"/"ouvinte". Frases curtas. Final em aberto, com uma pergunta para o público.
- **Marca verbal:** "o lado obscuro de…", metáforas de prisão, cela, sombra e luz.
- **"Sente-se. Hoje eu vou te mostrar o lado obscuro de…":** opcional. Só entra quando encaixa no gancho; não é obrigatório em todo vídeo.
- **Linha editorial (nov/2026):** o foco principal são **histórias e culturas antigas pelo lado feio e obscuro** (rituais, sacrifícios, costumes com os mortos), sempre com prova: relato de testemunha ou descoberta arqueológica/científica. Temas de fé e comportamento (como o bezerro) saem do foco. Pautas em `PAUTAS-CULTURAS-ANTIGAS.md`.
- **Equilíbrio:** em tema político, criticar o sistema e não um lado só. Mostrar contraponto. Não chamar o público de "gado".
- **Imagem recorrente do narrador:** `recomeço/a vida/Sorcerer_waiting_for_silhouette_…jpeg`.

## 2. Estrutura de pastas de um episódio

```
codex obscuro/
  codex-motion/              ← ferramenta (motor, thumbs, música)
  <episodio>/
    roteiro-<ep>.md          ← roteiro + tabela de fontes por linha (no fim)
    elevenlabs-<ep>.md       ← texto do ElevenLabs em "## Parte N", com <break>
    1.mp3 2.mp3 3.mp3 4.mp3  ← áudios de cada parte
    storyboard-parteN.txt
    imagens-para-gerar.md / videos-para-gerar.md
    imagens/  videos/  thumb/
    faixa 1.mp3 / faixa 2.mp3  ← músicas do Suno
```

## 3. Roteiro

- **Estrutura e ritmo:** seguir o `MODELO-DE-VIDEO.md` (frase 1 = título, cena 1 = thumb, gancho completo em 20 s, ciclos de energia, recompensa no final, troca de visual a cada 3 a 5 s). Rodar o checklist dele antes de gravar o áudio.
- **Storytelling:** antes do roteiro, preencher a **Ficha da história** (personagem, conflito, clímax, resolução, transformação, tema) da seção J do `MODELO-DE-VIDEO.md`. Cada vídeo é uma nova página do códex do Velho Contador.
- Duração: 7 a 14 minutos. Blocos com título e minutagem, indicação de cena em itálico e notas de produção.
- **Fontes:** tabela no FIM do arquivo (para não mudar a numeração), com linha · fala · tipo · o que mostrar no print · link.
- Dados só com fonte aberta e conferida. Percepção de mercado é escrita como "o mercado diz", não como dado.
- **ElevenLabs:** dividir em 4 partes de até 5 mil caracteres, números por extenso e pausas com `<break time="1.0s" />` (1,5 s em frases curtas de impacto, 2 a 3 s antes de virada).

### Gancho dos primeiros 15 segundos (OBRIGATÓRIO)
O paradoxo central ou a revelação principal aparece **nos primeiros 10 a 15 segundos**, antes da cena imersiva. A narrativa ("Pense na casa da sua avó…") vem **depois** do gancho, não no lugar dele.

Estrutura:
1. **0–5 s, a afirmação estranha:** valida o que o público sente e vira do avesso. Ex.: "Você não está imaginando. A luz de antigamente era mesmo diferente."
2. **5–12 s, o paradoxo ou revelação:** a ideia central do vídeo em uma frase. Ex.: "E ela não sumiu sozinha. Foi trocada. Mas a parte mais estranha é que metade dessa mudança está no mundo… e a outra metade está dentro da sua cabeça."
3. **12–15 s, a promessa:** o que a pessoa vai entender se ficar. Ex.: "Hoje eu vou te mostrar as duas."
4. Só então entra a cena lenta e imersiva.

Regras:
- Vale para todo vídeo, principalmente os nostálgicos e filosóficos, que tendem a começar devagar.
- O gancho tem no máximo 3 a 4 frases curtas, com `<break time="1.0s" />` entre elas, e não entrega a explicação, só o paradoxo.
- Precisa casar com a thumb e o título: o que a thumb pergunta, o gancho confirma nos primeiros segundos.
- No storyboard, o gancho usa clipe ou imagem forte + `texto:` com *destaque*, sem cartão de título (o título do vídeo vem logo depois).

## 4. Imagens (Flow)

**Estilo fixo (colar no fim de todo prompt):**
```
Minimalist white line art illustration on a solid pure black background. Clean white outlines of uniform thickness, no fill, no shading, no gray, no color, no text, no letters. Simple faceless human figures. Centered composition with generous empty black space around the subject. 16:9.
```
- Uns 28 a 45 por episódio. Podem vir com o nome do Flow: o Claude identifica cada uma pelo conteúdo e converte para PNG transparente (tira até fundo cinza).
- **Pessoas reais** (políticos etc.): mesmo tratamento para todos, expressão neutra, sem cara de vilão.

### Três camadas de imagem (a partir do Staden)
- **REAL:** gravura, página de livro, mapa antigo, foto de museu/escavação. Tratamento **B (documento)**: papel envelhecido, levemente torto, sombra, sobre o fundo hachurado + selo âmbar **"REGISTRO REAL"** com a fonte. Só material de domínio público ou com licença livre. Entra logo **depois** da frase forte, como prova.
- **IA (Flow):** cenas que ninguém registrou, no traço branco do canal. Pessoas sem rosto, nada de gore.
- **PALITOS:** explicação (mapas, ciclos, contagens) e simulação de fatos, com **"SIMULAÇÃO"** no canto.
- **Real primeiro (a partir do vídeo depois do Staden):** ~60% real, ~25% palitos, ~15% IA. A IA só entra onde não existe registro. A thumb usa a cena real mais marcante (foto da descoberta, do objeto, do lugar). Motivo: o Staden teve CTR de 0,3% em 590 impressões com thumb toda em line-art; o público não percebeu que era história real.
- **Licença das imagens reais (o canal é monetizado):** só domínio público, CC0, CC BY e CC BY-SA, com crédito na descrição. Nunca CC BY-NC ou ND, foto de agência de notícias, nem foto de museu sem licença aberta. Fontes: Wikimedia Commons, museus com acesso aberto (Met, Smithsonian, Rijksmuseum, Wellcome), NASA, Biodiversity Heritage Library, livros antigos digitalizados.

## 5. Clipes de vídeo (Flow, imagem → vídeo)

- De 4 a 6 por episódio, só nos momentos-chave: abertura, viradas e fechamento.
- Duração = tempo da cena arredondado para cima (4/6/8/10 s). Na dúvida, 8 s.
- Prompt sempre com: câmera parada ou lenta, sem cortes, mesmo estilo line-art, fundo preto, sem texto.
- Salvar em `videos/clip-NN-nome.mp4`. Se faltar o clipe, entra a imagem parada.
- A ferramenta mantém a cor original do clipe (ex.: janela acesa em âmbar).

## 6. Motion (codex-motion)

- **Fundo:** `codex-motion/fundo.jpeg` (hachurado), com movimento lento, vinheta e grão fixo.
- **Fontes:** Cinzel (títulos), Cormorant Garamond (frases), Special Elite (créditos de fonte), Anton (thumbs).
- **Cor de destaque por episódio** (`--destaque`): `vermelho` = política/tensão (Favorzinho), `ambar` = memória/nostalgia (Até a luz). Também aceita `azul` ou `#RRGGBB`.
- **Storyboard:** um título de capítulo a cada bloco, frase de impacto curta com *destaque*, contador para todo número (22%, 68%…) com `fonte:`, e imagem com `legenda:` quando citar livro, estudo ou lei.
- **Render no PC:** em pedaços de até ~60 s com `--sem-audio`, depois `juntar` com os 4 áudios. Na última parte, `--fade-final`. 1080p a 30 fps.

- **Sub-cenas (`+ palavra`):** dentro de um trecho longo, `+ palavra` troca o visual quando aquela palavra é falada. Serve para cumprir a regra de trocar o visual a cada 3 a 5 s.
- **Selo no canto (`--selo imagem.png` + `selo: 0 a 1`):** imagem fixa no canto superior direito, na cor de destaque, cujo brilho muda ao longo do vídeo. É o "motivo recorrente" do modelo (no Adão, a silhueta perde brilho a cada poder perdido e acende de novo nas unhas).

### Animação no lugar de texto (a partir do Enoque)
- Frases de impacto viram **cenas curtas de palitos animadas** pelo Claude, em vez de texto em português na tela (que a legenda e a dublagem não traduzem). Números, relógio, símbolos e crédito de fonte continuam. Capítulos = numeral romano + ícone. Detalhes na seção E do `MODELO-DE-VIDEO.md`.

### Chamada de like + inscreva-se
- Card animado no canto inferior direito (`chamada.py`): cursor clica no like e no INSCREVA-SE, que vira INSCRITO e faz o sino balançar. Usa a cor de destaque e dura cerca de 6 s.
- **2 vezes por vídeo:** perto de 2:00 e perto do final, antes da última reflexão. Em cena de texto centralizado, sem legenda embaixo.
- Uso: `render ... --chamadas 0.6` (segundos dentro daquela parte).

## 7. Música de fundo (Suno) — PADRÃO APROVADO

- Instrumental ligado. Gerar 2 ou 3 versões e escolher a mais calma e constante.
- Duas faixas quando o tema tem virada de clima. Uma só quando o clima é contínuo.

**Faixa quente** (memória, abertura, fechamento):
```
nostalgic ambient, warm analog synth pads, soft felt piano, gentle vinyl crackle, slow tempo 60 bpm, dreamy, melancholic but comforting, old home memories, cinematic underscore, minimal, no drums, instrumental
```
**Faixa fria** (tensão, sistema, obscuro):
```
dark minimal ambient, cold sterile synth drones, distant metallic textures, sparse low piano notes, slow tempo 55 bpm, eerie, mysterious, empty modern city at night, cinematic underscore, no drums, no melody hooks, instrumental
```

**Mixagem** (`codex-motion/mixar_musica.py`):
- **Volume da música: -27 dB**, o padrão do script. Resultado medido: voz a -14,7 dB e música a -38 dB nas pausas, uns 23 dB abaixo da voz.
- Ducking automático: a música abaixa mais quando o narrador fala.
- Transição de 3 s entre faixas. Faixa curta é emendada nela mesma com fade de 8 s.
- Volume final -14 LUFS (padrão YouTube).
- Exemplo:
```
python3 codex-motion/mixar_musica.py --video video_com_voz.mp4 \
  --trilha "ep/faixa 1.mp3:0:126" --trilha "ep/faixa 2.mp3:126:330" --trilha "ep/faixa 1.mp3:330:fim:55" \
  --saida final.mp4
```


### Trilha própria (gerada em código) — usada a partir de "Paralisia do sono"
- O Claude sintetiza a música no código (`codex-motion/trilha_paralisia.py` é o modelo): grave contínuo, pads de acordes, caixinha de música, pulsos, coração, impactos e silêncios **sincronizados com os momentos do roteiro**. Sem direitos autorais.
- Mapa de tensão por bloco: começa baixa, impactos nas frases-chave, pico antes da revelação, 1 s de silêncio total depois do pico, e resolução calma (acorde maior) no fechamento.
- **Como a trilha conversa com o vídeo** (referência: análise do vídeo da Amazônia profunda):
  - **Cama de som do tema:** além da música, um som "do mundo" do episódio (relógio e respiração na Paralisia, vento e areia num vídeo bíblico, cigarras numa floresta).
  - **Tensão antes da transição:** nos 1 a 3 s antes de uma transição forte, esse som de ambiente e a música **crescem** (subida).
  - **Contraste depois da transição:** logo depois vem um **drop** ou uma troca de textura (orgânico → mecânico/percussivo, ou cheio → quase vazio).
  - **Acompanha a fala:** em montagens e listas, um pulso ou percussão leve acelera junto com a voz; em frases de impacto e reflexões, a música **some ou fica só um grave**, para a frase pesar.
  - O gerador da trilha lê os tempos das transições (`*.transicoes.json`) e das falas (alinhamento) e posiciona subidas, drops e silêncios sozinho.
- **Mixagem padrão (aprovada em 19/out, "teste C"): `--voz-tv --volume -14 --teto-trilha -21 --ducking 2.5 --lufs -13`** (ajustado no mesmo dia: trilha 3 dB mais baixa e com teto de pico, para nenhum impacto passar a voz). A voz passa por equalização (menos grave sobrando, mais 3 kHz) e compressão leve, para ser entendida na TV (46% do tempo do faraó foi na TV). A trilha fica mais alta e quase não abaixa debaixo da voz. O -27 continua valendo só para músicas do Suno.
- **A trilha é contínua do começo ao fim** (cama de acordes + arpejo de oud + percussão + melodia), mudando a cada bloco do roteiro. Silêncio só nos buracos de 1 a 2 s depois das frases de impacto.
- **Toda animação tem efeitos sonoros** (fogo, moedas, multidão, vento, passos, páginas…) num arquivo próprio (`fx-*.wav`), gerado pelo `codex-motion/sfx_lib.py` e misturado com a voz a 0 dB, com teto de pico (nenhum efeito passa a voz). As animações são feitas já sabendo em que segundo cada som acontece.

### Curta animado de abertura (opcional)
- Abertura de 30 a 40 s, sem narração, animada em código no estilo "palito" com traço branco (`codex-motion/curta_paralisia.py` é o modelo), com sons sintetizados. A primeira cena mostra o que a thumb promete.

## 8. Thumbnail

- **Estilo A, fogo vermelho** (`thumb.py`): fundo de fogo vermelho + hachurado, figuras em silhueta preta com traço branco e borda vermelha brilhante, figura principal no centro e maior. Texto Anton com 1 palavra em vermelho.
- **Estilo B, meme "Não grita"** (`thumb_meme.py`): fundo escuro granulado, texto itálico grosso. Pode levar o fogo vermelho por cima.
- Retratos em close (cabeça e ombros) funcionam muito melhor que corpo inteiro.
- Texto curto, de 2 a 4 palavras, que não repita o título.
- Gerar 2 versões para usar no "Testar e comparar" do YouTube Studio.

## 9. Publicação

- **Título:** em maiúsculas, **até 50 caracteres**, curto e forte, que complete a thumb em vez de repetir.
- **Descrição:** gancho de 2 linhas, resumo, capítulos (tempos tirados das emendas dos áudios), fontes e 3 hashtags (tema em alta, tema do vídeo, #CódexObscuro).
- **Tags:** termos do Google Trends (buscas em ascensão) + termos explicativos ("o que é…").
- **Horário:** de manhã (8h–10h), subindo o arquivo na noite anterior para o HD processar. Comentário fixado com uma pergunta.

## 10. Limitações conhecidas

- O Claude não apaga arquivos no seu PC: sobras (`render/`, JPGs, clipes com nome do Flow) ficam para você apagar.
- O Google Trends às vezes bloqueia por excesso de acessos. Tentar de novo depois de um tempo.
- APIs de geração de imagem (OpenAI, Google, Higgsfield) ficam bloqueadas no ambiente do Claude. As imagens são geradas por você no Flow.
