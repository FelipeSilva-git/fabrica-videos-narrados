---
name: pesquisa-google-trends
description: Pesquisar no Google Trends (Web e YouTube) o que as pessoas estão buscando sobre um tema de vídeo - tendência, consultas em ascensão e principais, comparação de termos - antes de definir pauta, título e tags.
---

# Pesquisa no Google Trends

Use **sempre** antes de propor pauta, título ou thumb, mesmo quando a pessoa já trouxe o tema.

## Ferramenta
- O Google Trends costuma bloquear acesso automático (WebFetch/curl). Use o **navegador interno** do Claude; se não houver, o **Claude in Chrome**.
- Sem navegador ou com bloqueio/captcha: diga isso, peça um print ou que a pessoa libere o navegador, e faça uma pesquisa **parcial** com o autocompletar do YouTube + busca na web. Nunca complete os números de memória.

## Passos
1. País e idioma: do `canal/PERFIL-DO-CANAL.md` (ex.: `geo=BR`).
2. Pesquisa na Web: `https://trends.google.com/trends/explore?geo=BR&date=today%2012-m&q=<termo>`
3. Pesquisa do YouTube: mesma URL + `&gprop=youtube`.
4. Compare até 5 termos separados por vírgula em `q=` (tema, variações, temas vizinhos).
5. Em cada página, leia como texto (ou role até os blocos) e anote:
   - tendência do interesse (subindo / estável / caindo, picos e o motivo provável);
   - **Consultas relacionadas → Em ascensão** (com %) e **→ Principais**;
   - assuntos relacionados; sub-região com mais interesse.
6. Autocompletar do YouTube para o tema + os 3–5 vídeos mais vistos (ângulo que já foi usado).

## Saída
Preencha `modelos/pesquisa-de-tendencias.md` na pasta do episódio (com a data da consulta) e termine com:
- **ângulo** sugerido a partir de uma consulta em ascensão;
- **palavras** para título, descrição e tags (das principais);
- **alerta** se o tema estiver caindo ou sem busca.

## Cuidados
- O Trends mostra interesse **relativo (0–100)**, não volume. "Aumento repentino" = crescimento acima de 5.000%.
- Interesse muito baixo pode não ter dados; tente um termo mais amplo.
- Cite a data: tendências mudam em dias.
