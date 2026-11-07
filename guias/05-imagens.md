# 05 · Imagens: real primeiro

## Três camadas
| Camada | O que é | Tratamento | Proporção |
| --- | --- | --- | --- |
| **REAL** | foto de museu, escavação, gravura, página de livro, mapa antigo | **documento**: papel, leve rotação, sombra, selo "REGISTRO REAL" + autor + licença (`motor/imagens/documento.py`) | ~60% |
| **ANIM** | palitos animados em código: explicação, mapa, contagem, simulação | traço do canal; "SIMULAÇÃO" no canto quando reconstrói um fato | ~25% |
| **IA** | cenas que ninguém registrou | estilo fixo do perfil (prompt-base), pessoas sem rosto, nada de gore | ~15% |

A IA só entra onde **não existe registro**. A imagem real entra **logo depois** da frase forte, como prova.

## Licenças (canal monetizado)
✅ Domínio público · CC0 · CC BY · CC BY-SA — **sempre com crédito** (no selo e na descrição).
❌ CC BY-NC · CC BY-ND · foto de agência de notícias · foto de museu sem licença aberta · "achei no Google".

Fontes boas: Wikimedia Commons, museus com acesso aberto (Met, Smithsonian, Rijksmuseum, Wellcome Collection), NASA, Biodiversity Heritage Library, livros antigos digitalizados (Internet Archive, Biblioteca Nacional).

## Fluxo com o Commons
```bash
python3 motor/imagens/commons.py buscar episodios/ep "Llullaillaco mummy" "Inca capacocha" "Salta museum"
#  -> commons.json (só licenças aceitas). Escolha e liste os títulos em selecao.txt
python3 motor/imagens/commons.py baixar episodios/ep selecao.txt
#  -> imagens-reais/r01-...jpg + CREDITOS.md
python3 motor/imagens/documento.py episodios/ep/imagens-reais episodios/ep/imagens-reais/CREDITOS.md episodios/ep/imagens [--sepia]
#  -> imagens/doc-r01.png ...   (no storyboard: documento: imagens/doc-r01.png)
```
- Busque em inglês e no idioma local do tema; tente o nome científico/do museu.
- O Commons limita acessos (erro 429): o script espera; se faltar alguma, rode de novo mais tarde.
- **Confira cada imagem com os olhos** antes de usar (às vezes o título engana) e confira a licença na página.
- Imagem sensível (restos humanos): respeito. Mostre o necessário para a prova, sem close gratuito.

## Imagens de IA (a pessoa gera)
O Claude escreve `imagens-para-gerar.md` (use `modelos/imagens-para-gerar.md`): código, cena do roteiro, prompt, e o **prompt-base de estilo do perfil** no fim de cada prompt. Se o gerador recusar um prompt, reescreva tirando o elemento sensível (ex.: cordas no pescoço) e mostrando o momento antes/depois.

Clipes (imagem → vídeo): 3–6 por episódio, só em viradas. Câmera parada ou lenta, sem cortes, mesmo estilo, sem texto. Duração = tempo da cena arredondado para cima (4/6/8 s).

## Thumb com foto real
Use a cena real mais marcante (a descoberta, o objeto, o rosto). Camadas: foto real tratada + um elemento do estilo do canal (line-art, brilho) com **borda esfumada**, texto curto grande.
