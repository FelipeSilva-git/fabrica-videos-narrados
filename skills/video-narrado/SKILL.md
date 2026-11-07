---
name: video-narrado
description: Produzir um vídeo longo narrado de YouTube (história, documentário, mistério, ciência) para qualquer canal - pauta, título e thumb, roteiro com retenção, voz Gemini TTS, storyboard, motion, trilha, mix e publicação - usando o kit fabrica-videos-narrados.
---

# Vídeo narrado (qualquer canal)

## Antes de tudo
1. Procure o kit `fabrica-videos-narrados` (pasta com `CLAUDE.md`, `guias/`, `motor/`, `canal/`). Se existir, **leia o `CLAUDE.md` dele e siga**. Se não existir, peça o repositório ou trabalhe com as regras resumidas abaixo.
2. Leia `canal/PERFIL-DO-CANAL.md`. Vazio → entreviste a pessoa e preencha antes de produzir. Preenchido → ele manda sobre os padrões gerais.
3. Leia `canal/REGISTRO-DE-VIDEOS.md`: lições anteriores valem como regra.

## Pipeline (🔒 = aprovação da pessoa)
pauta 🔒 → **embalagem antes do roteiro** (entrega, gatilhos, 3 títulos ≤ 50 caracteres, esboço de thumb) 🔒 → ficha da história → roteiro com mapa visual REAL/ANIM/IA e tabela de fontes 🔒 → voz (parte 1 primeiro) 🔒 → imagens reais licenciadas + prompts de IA para a pessoa gerar 🔒 → alinhamento → ritmo → storyboards → animações → render por partes → trilha + fx → mix -13 LUFS → QA de quadros → publicação → registro após 48 h / 7 dias.

## Regras resumidas
- **Promessa (0–5 s):** cena 1 = thumb em movimento, frase 1 ecoa o título, entendível sem som. Nunca "olá"/vinheta.
- **Gancho (≤ 20 s):** contexto, o que está em jogo, lacuna, esforço com número verdadeiro, "e não é só isso".
- **Corpo:** ciclos ALTA → BAIXA → GANCHO; revelações crescendo; algo novo a cada ~3 min; parte mais forte nos últimos 20%; fonte curta e depois da revelação; terminar logo após a recompensa; fechamento circular.
- **Storytelling:** personagem (quer/impede), conflito no gancho, clímax, resolução, transformação ("você nunca mais vai ver ___ do mesmo jeito"), identificação com o que o público já viveu.
- **Visual:** troca a cada 3–5 s (sub-cenas `+ palavra`); **animação no lugar de texto**; real primeiro (~60/25/15); transições só com motivo (corte depois de frase de impacto).
- **Gatilhos de clique:** autoridade, contradição, novidade (escassez quase nunca). Contradição em frase venceu palavra solta no A/B. Thumb de história real usa **foto real**.
- **Voz Gemini:** estilo como notas do diretor + `#### TRANSCRIPT`; pausas por parágrafo; números por extenso; ≈0,29–0,37 s/palavra.
- **Mix:** voz para TV, trilha contínua com teto, fx com limitador, -13 LUFS.
- **Licenças de imagem:** só PD, CC0, CC BY, CC BY-SA com crédito (ver skill `imagens-reais-licenciadas`).
- **Chaves de API:** só por variável de ambiente; nunca exibir nem versionar.
- **Uma melhoria por vídeo**, anotada no registro.
