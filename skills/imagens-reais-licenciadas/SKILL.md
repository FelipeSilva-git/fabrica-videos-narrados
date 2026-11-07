---
name: imagens-reais-licenciadas
description: Encontrar, baixar e creditar imagens reais (fotos de museu, escavações, gravuras, mapas antigos) com licença livre para uso em vídeo monetizado - Wikimedia Commons e acervos abertos - e tratá-las como "documento" com selo de crédito.
---

# Imagens reais com licença livre

## Licenças
- ✅ Domínio público, CC0, CC BY, CC BY-SA — sempre com crédito (autor + licença) no vídeo e na descrição.
- ❌ CC BY-NC, CC BY-ND, fotos de agências de notícias, fotos de museu sem licença aberta, imagens "do Google".
- Confira a licença **na página do arquivo**, não só no resultado da busca.

## Onde procurar
Wikimedia Commons (principal), Met Open Access, Smithsonian Open Access, Rijksmuseum, Wellcome Collection, NASA, Biodiversity Heritage Library, Internet Archive (livros antigos), bibliotecas nacionais.

## Fluxo (kit fabrica-videos-narrados)
```bash
python3 motor/imagens/commons.py buscar <ep> "termo em inglês" "termo local" "nome do museu"
# leia commons.json, escolha as que provam cada fala do roteiro, liste os títulos em selecao.txt
python3 motor/imagens/commons.py baixar <ep> selecao.txt          # imagens-reais/rNN-*.jpg + CREDITOS.md
python3 motor/imagens/documento.py <ep>/imagens-reais <ep>/imagens-reais/CREDITOS.md <ep>/imagens [--sepia]
# storyboard: documento: imagens/doc-rNN.png
```
Sem o kit: use a API do Commons (`action=query&generator=search&gsrnamespace=6&prop=imageinfo&iiprop=extmetadata|url&iiurlwidth=1280`) e filtre por `LicenseShortName`.

## Boas práticas
- Busque por **prova**: a imagem entra logo depois da frase que ela comprova.
- Olhe cada imagem antes de usar (títulos enganam); descarte arquivos vazios.
- Erro 429: espere e repita; use miniaturas de tamanho padrão (1280 px).
- Restos humanos e vítimas: respeito; sem close gratuito.
- Na descrição: "rNN — Autor, Licença (Wikimedia Commons)". Se passar de 5.000 caracteres, tire as URLs.
- A thumb de história real usa a **foto real mais marcante**.
