# CANAL TESTE — Modelo de vídeo

Baseado no que o MrBeast ensina sobre ideia, título, thumb, gancho e retenção (meta: **70% de retenção**), adaptado para vídeo **narrado com motion** e para um canal pequeno que quer crescer também fora do Brasil.
Use junto com o `PADROES-DO-CANAL.md`. Este arquivo diz **o que fazer e em que ordem**; os padrões dizem **o estilo**.

> Resumo em uma linha: **o YouTube só quer que as pessoas cliquem e assistam.** Toda regra abaixo serve a uma dessas duas coisas. Quando alguém disser "o algoritmo não gostou", troque por "o público não gostou".

---

## A. A ideia

**De onde vêm as ideias:**
- **Google Trends** (buscas do YouTube no Brasil, como já fazemos) e os comentários dos próprios vídeos.
- **Dieta de informação:** reservar tempo para consumir com intenção de aprender (livros, artigos, documentários, canais de fora). Se a gente só consome o que já conhece, as ideias começam a se repetir.
- **Caderno de ideias:** toda ideia vai para uma lista, mesmo incompleta. Escolher é mais fácil do que inventar na hora.

**O filtro: uma ideia só passa se for as três coisas.**
1. **Interessante para o nosso público** (mistério, lado obscuro, coisas que todo mundo sente e ninguém explica).
2. **Original:** ninguém contou desse jeito. "O que é paralisia do sono" é genérico; "por que todos veem a mesma criatura" é original.
3. **Forte / extrema:** a versão mais intensa da ideia. Entre "correr uma maratona" e "escalar uma montanha", escolha a montanha.

**As duas linhas que o YouTube já entrega para o canal** (relatório de 15/out): o algoritmo coloca os vídeos ao lado de
1. **Bíblia oculta e textos proibidos** (Enoque, Adão, gnosticismo, profetas) → melhor retenção.
2. **Terror e mistério real** (Paralisia, Amazônia, criaturas, encontros) → vizinhos com CTR de 19–40%.
Ideia nova tem que cair numa dessas duas. Autoajuda e política trazem clique de fora do nicho e não seguram. Cada vídeo longo ganha um **Short-isca** do mesmo tema.

**Se não sair um título e uma thumb bons, a ideia não é produzida.** Melhor descartar no papel do que depois de pronto.

---

## B. Título e thumb (a embalagem) — sempre ANTES do roteiro

### Título
- **Até 50 caracteres.** Acima disso, em alguns celulares aparece "…" e a pessoa nem sabe no que está clicando.
- **Curto, simples e forte.** Não "a paralisia do sono é estranha", e sim uma afirmação ou pergunta que incomoda: "POR QUE TODOS VEEM A MESMA CRIATURA?".
- **Fica na cabeça:** se a pessoa não clicar, ela continua pensando nele.
- **Combina com a duração:** a promessa tem que valer os 7 a 10 minutos do vídeo.
- **Não repete a thumb:** título e thumb contam juntos uma história; cada um diz uma parte.

### Thumb
- **Esboço antes da produção:** o Claude faz um rascunho rápido da composição antes de pedir as imagens.
- **Cada elemento tem um motivo** e é **distinto**: nada se mistura com o fundo, a silhueta do personagem é clara, sem poluição.
- **Uma emoção só:** curiosidade, medo, espanto. A pessoa entende o conceito em meio segundo, rolando a tela.
- **Contraste alto:** nosso estilo é escuro, mas o assunto principal precisa ser **claro e brilhante** (ex.: Adão brilhando, criatura com contorno de luz). No teste A/B, vale testar uma versão mais clara.
- Texto de 1 a 3 palavras, grande, com o personagem na frente das letras quando der (`thumb_titulo_atras.py`).

### Checklist da embalagem
- [ ] Título com até 50 caracteres.
- [ ] Esboço da thumb aprovado.
- [ ] Escrever em uma frase: **"Quem clicar espera ver ______."**
- [ ] Escrever a **pergunta que só será respondida no fim** (a lacuna de curiosidade).

---

### Os 4 gatilhos do clique (das skills dos outros projetos, nov/2026)
Gatilho sem entrega é clickbait. Escolher **antes** do roteiro e marcar no roteiro onde a promessa é paga.
| Gatilho | Sensação | No Arquivo |
| --- | --- | --- |
| **Autoridade** | "essa pessoa sabe" | testemunha ocular, livro antigo, estudo (DNA, cabelo da múmia), com a fonte na tela |
| **Contradição** | "como assim?" | "não era fome", "a lenda estava errada": coloca uma crença à prova e explica o mecanismo |
| **Novidade** | "isso é novo" | só com descoberta recente de verdade (ex.: DNA de 2024) |
| **Escassez** | "pode passar" | quase nunca se aplica; não forçar |
**Folha de aplicação (no topo de todo roteiro):** (1) a entrega concreta; (2) os gatilhos; (3) 3 títulos: A = um gatilho, B = a mesma promessa de outro jeito, C = dois gatilhos; (4) o que a thumb mostra. O título fala, a thumb mostra, e eles nunca repetem o mesmo texto.

### Técnicas emprestadas do formato "E se…?"
- **Flash-forward no gancho:** mostrar o momento mais tenso antes de voltar ao começo.
- **Plantar e pagar:** um elemento aparece cedo e volta depois com outro sentido (o navio que recusa e o navio que salva).
- **O jeito ingênuo falhando antes da solução:** cada tentativa do personagem falha até a que funciona.
- **Uma cena forte por bloco.**
- **Uma voz só:** as falas dos personagens o Narrador lê no tom deles, e elas aparecem escritas na tela.

## C. Primeiros 5 segundos: cumprir a promessa (e vender o clique)

Na página inicial, o YouTube **toca o vídeo sozinho, sem som e com legenda**. Muita gente decide clicar vendo esses primeiros segundos, sem nem olhar a thumb. Então:

| O quê | Regra |
| --- | --- |
| **Primeira cena** | É a **thumb em movimento**: mesma figura, mesmas cores, mesma composição. |
| **Primeira frase** | Combina com o **título**. Quem leu o título reconhece a frase. |
| **Sem som** | Os 5 primeiros segundos precisam ser entendidos **só com a imagem e a legenda**. |
| **Claro, não obscuro** | Ganchos claros funcionam melhor que ganchos confusos. Mistério sim, confusão não. |
| Proibido | Começar com "Olá", nome do canal, vinheta ou contexto histórico. |

## D. Até 20 segundos: o gancho completo

1. **Contexto:** do que é o vídeo, numa frase.
2. **O que está em jogo / recompensa:** o que a pessoa vai saber ou sentir se ficar.
3. **Lacuna de curiosidade:** uma pergunta que só se resolve no final.
4. **Esforço visível:** mostrar o trabalho que deu, **sempre com números verdadeiros** ("reuni nove textos", "35 pesquisas, 36 mil pessoas").
5. **Superar a expectativa:** entregar o prometido logo e mostrar que vem **mais** ("e não é só isso…").

- **Muitos cortes nos primeiros 30 s:** é onde se perdem 30% das pessoas. Cada 10% a menos de perda aqui vale mais do que melhorar o vídeo inteiro.
- **Aos 20 s, o primeiro ponto já começou.**
- O "Sente-se…" é **opcional**: só entra quando encaixa e cabe nos 20 s.
- **Curta de abertura (opcional):** 30 a 40 s animados sem narração, quando o tema pede (ex.: Paralisia do sono). A primeira cena do curta é a thumb.

---

## E. Regra visual nova: animação no lugar de texto

O texto em português na tela **não é traduzido** pela legenda nem pela dublagem automática, e ainda **disputa a parte de baixo da tela com a legenda**. Nos dados do canal, quem assiste com legenda (em português ou inglês) vê só **metade** do vídeo, comparado a quem assiste sem.

**A partir do próximo vídeo (teste: Enoque):**

| Antes | Agora |
| --- | --- |
| Frase de impacto escrita ("Foi uma *vingança*") | **Cena curta de palitos animada pelo Claude**, mostrando a ideia (o anjo virando as costas, a serpente se aproximando) |
| Cartão de capítulo com título em palavras | **Numeral romano grande + ícone** (I, II, III…) |
| Legenda explicativa embaixo da imagem | Sai. A narração e a dublagem explicam |
| Números (35, 7,6%, 1781) | **Continuam** (números são universais) |
| Relógio, símbolos, setas | **Continuam** |
| Crédito de fonte no canto | **Continua**, pequeno, no canto de cima |

O roteiro passa a ser escrito pensando em **"o que dá para mostrar"**, e não "o que dá para escrever". A parte de baixo da tela fica livre para a legenda.

---

## F. Corpo: ciclos de energia e retenção

```
ALTA   → revelação forte de abertura do bloco (imagem nova, animação, clipe ou número)
BAIXA  → explicação, prova, fonte, exemplo
GANCHO → frase que puxa o próximo bloco ("mas isso não é o mais estranho…")
```

| Duração do vídeo | Ciclos | Tamanho de cada ciclo |
| --- | --- | --- |
| 6 a 9 min | 5 a 6 | 1 a 1,5 min |
| 10 a 14 min | 6 a 8 | 1,5 a 2,5 min |

- **Escalada:** cada revelação mais forte que a anterior. A mais forte fica para o fim.
- **Grande recompensa no final:** é ela que segura a pessoa num momento mais fraco do meio.
- **História paralela:** em vídeos longos, um único fio cansa. A cada ~3 min, algo novo reengaja: o **motivo recorrente** (o selo do Adão, o relógio 03:07), um curta, uma virada.
- **O começo é o que mais importa:** quem passa da metade tende a ir até o fim. O maior esforço vai para o primeiro terço.
- **Parte sombria ou emocional** só nos **últimos 20%**.

### Variedade visual (regra dos 3 a 5 segundos)
- **Nenhuma tela parada por mais de 5 s.** Usar sub-cenas (`+ palavra`) para trocar o visual no meio das frases longas.
- Imagem repetida volta com **outro efeito ou enquadramento**.

### Contraste constante (tipos de cena)

| Tipo | Uso |
| --- | --- |
| Imagem line-art + narração | Base do vídeo |
| **Animação de palitos** | Frases de impacto, revelações (substitui o texto) |
| Número / contador | Dado forte |
| Clipe de vídeo (3 a 6 por episódio) | Viradas e momentos-chave |
| Motivo recorrente (selo, relógio) | Costura o vídeo |
| Tela preta + silêncio (1 a 2 s) | Antes da maior revelação |


### Transições com som (a partir do Enoque)
Cada troca importante de cena tem um **tipo de transição** e um **som próprio** (`transicao:` no storyboard; os sons saem do `sfx_transicoes.py`).

| Transição | Visual | Som | Quando usar |
| --- | --- | --- | --- |
| Fusão (padrão) | Uma imagem dissolve na outra | Nenhum | Explicação calma, dentro do mesmo bloco |
| `whip` | Chicote: a tela "voa" para o lado com rastro | Whoosh | Listas e montagens rápidas (países, exemplos, datas) |
| `corte` | Corte seco | Batida grave curta | Depois de uma frase de impacto ou de um silêncio |
| `zoom` | Soco de zoom para dentro | Subida + impacto | Revelação, número forte |
| `flash` | Clarão branco | Impacto + brilho agudo | Grande revelação, abertura de capítulo |
| `glitch` | Imagem tremendo e com cores separadas | Ruído digital | Criatura, algo "errado", terror |

- **Só onde faz sentido:** a transição precisa ter um motivo na história (lista → whip, revelação → zoom/flash, criatura → glitch, frase de impacto → corte). Nunca por enfeite.
- **Variar os tipos** e usar **no máximo uma transição forte a cada 10 a 15 s**. A mesma transição repetida vira vício; se tudo tiver efeito, nada tem impacto.
- **Aprovado no teste:** o corte seco com batida depois de frase de impacto funciona muito bem. Usar sempre que houver uma frase de peso.
- **Antes da transição, o som cresce** (tensão); **depois dela, muda o clima** (o drop). A trilha própria já é feita sabendo onde estão as transições.

### O que os dados do canal já mostraram
- **Fonte com data e nome comprido derruba a retenção.** Primeiro a revelação estranha, depois a fonte em meia frase ("…diz um texto judaico antigo"). O nome completo e a data ficam no crédito do canto.
- **O lado obscuro puxa gente para frente:** no Adão, a retenção **subiu** quando começou "O lado obscuro". Prometer essa parte já no gancho e não deixar para muito tarde.
- **Depois da recompensa, terminar rápido.** Avisos e ressalvas ("nada disso está na Bíblia…") entram antes, no meio do vídeo, nunca depois da grande revelação.

### Ritmo da voz
O ElevenLabs lê o texto do jeito que ele está escrito, então o ritmo é decidido no texto:
- **Montagens e listas** (vários exemplos seguidos): uma frase só, com vírgulas e **sem pausas** entre os itens. A voz acelera naturalmente.
- **Frases de impacto**: sozinhas na linha, curtas, com **pausa de 1,5 a 2,5 s antes e depois**. A voz desacelera e a frase pesa.
- **Explicação**: ritmo constante, pausas de 1 s.
- Alternar os três ao longo do vídeo: o contraste entre rápido e lento é o que prende.

---

## G. Final: recompensa e terminar em alta

1. **Grande recompensa:** responde a lacuna do gancho.
2. **Terminar em alta:** imagem final forte e frase curta. Sem despedida longa.
3. **Pergunta para os comentários** e **gancho do próximo vídeo**.
4. Like + inscreva-se: perto de 2:00 e antes da última reflexão.
5. **Tela final apontando para a playlist** (fazer a pessoa **continuar assistindo** é a terceira coisa que o YouTube mede).

---

## H. Pós-produção: cortar o que é chato

- [ ] Assistir o vídeo inteiro **de uma vez** e anotar todo momento em que deu vontade de pegar o celular.
- [ ] Mostrar para 1 ou 2 pessoas **bem críticas** e observar onde elas se distraem. Pedir para "detonarem" o vídeo.
- [ ] Em cada ponto anotado: cortar a frase ou trocar o visual.
- [ ] Conferir: nenhuma tela parada por mais de 5 s; os primeiros 5 s funcionam sem som; o primeiro ponto começa antes dos 20 s.
- [ ] **48 h e 7 dias depois:** anotar a retenção no registro abaixo, por idioma de legenda e por faixa de áudio (dublagem).

---

## I. Como o canal cresce

- **Qualidade antes de quantidade:** é melhor 1 vídeo por semana muito bom do que 3 medianos. Um vídeo mediano não estoura; um muito bom obriga o YouTube a recomendar.
- **1 melhoria por vídeo:** a regra dos "100 vídeos" — cada vídeo melhora **uma coisa** (roteiro, gancho, thumb, som, animação…). A melhoria fica anotada no registro.
- **Não ficar preso ao calendário:** se o vídeo não está bom, atrasar 2 dias é melhor do que publicar mediano.
- **Grupo de criadores (mastermind):** o maior acelerador do MrBeast foram 4 amigos criadores estudando juntos todo dia. Vale achar 2 a 4 canais pequenos de mistério ou curiosidade para trocar análises toda semana (thumbs, retenção, títulos). Enquanto isso, o Claude faz o papel de crítico a cada vídeo.

---

## J. Storytelling: os 8 elementos de toda história

Todo vídeo é uma **história**, não só um tema. Antes de escrever o roteiro, conferir os 8 elementos:

| Elemento | O que é | Como fica no canal |
| --- | --- | --- |
| **1. Personagem** | Alguém no centro, com motivação clara | Enoque, Adão, a pessoa na cama. Responder: **quem é, o que quer, o que o impede** |
| **2. Conflito** | Uma força contra outra; é o que gera emoção e curiosidade | Vigilantes × céu, livro × Igreja, mente acordada × corpo travado. **Aparece já no gancho (até 20 s)** |
| **3. Enredo** | Começo, meio e fim numa sequência clara | Esqueleto de roteiro + ciclos de energia (seção F) |
| **4. Clímax** | O ponto de maior tensão; sem ele o vídeo fica morno | A maior revelação, nos últimos 20% (ex.: "Uma prisão." + colunas de fogo) |
| **5. Resolução** | O conflito se fecha; o público não fica sem fechamento | A recompensa que responde a lacuna do gancho (seção G) |
| **6. Transformação** | O personagem, e quem assiste, sai diferente | No vídeo: algo muda de estado (Enoque some na luz; o livro sai das correntes e vai para o altar). No público: **"depois deste vídeo, você nunca mais vai ver ______ do mesmo jeito"** |
| **7. Tema** | A grande ideia que liga tudo | Do canal: **"o que foi escondido de você"**. De cada vídeo: uma frase só |
| **8. Tom e voz** | Tom = jeito de contar; voz = identidade de quem conta | Tom misterioso e investigativo; voz do **Narrador** |

### Ficha da história (preencher antes do roteiro)
```
Personagem:     quem é / o que quer / o que o impede
Conflito:       ______ contra ______
Clímax:         a cena de maior tensão
Resolução:      como a lacuna do gancho se fecha
Transformação:  o que muda no vídeo + "você nunca mais vai ver ______ do mesmo jeito"
Tema (1 frase): ______
Identificação:  o que a maioria do público já viveu ou ouviu sobre isso
```

### O arco do Narrador (fio da série)
O narrador também é um personagem com história: ele está montando um **arquivo** com o que foi apagado. Cada vídeo é **uma página nova** desse arquivo (Adão → Enoque → nefilins…).
- Abertura ou fechamento pode mostrar a página sendo acrescentada (ícone, selo ou animação curta).
- O fechamento sempre aponta a **próxima página** ("e ele é o próximo").
- Isso dá motivo para assistir o próximo vídeo e para maratonar a playlist.

### Identificação nos primeiros segundos
O jeito mais rápido de segurar alguém na introdução é **ligar o tema a algo que a maioria do público já viveu ou já ouviu**.
- Conhecer o público: YouTube Studio → **Público** (idade, gênero, país, o que mais assistem). Revisar a cada 5 vídeos.
- Achar o **ponto de conexão** e ligar ao assunto: "você já ouviu falar da maldição da múmia", "todo mundo já acordou sem conseguir se mexer", "você já leu a Bíblia inteira e nunca viu esse livro".
- Não precisa servir para 100% das pessoas, só para **a maioria**.
- Vale pedir no meio do vídeo: "se isso já aconteceu com você, comenta aqui". Isso gera comentários e confirma o ponto de conexão.

### Storytelling não é uma sequência de fatos
Uma lista de acontecimentos ("ele nasceu, foi para o Egito, abriu a tumba, morreu") é chata. Vira história quando existe **missão, risco, desafio e expectativa**. Storytelling não é inventar nada: é **organizar o que já temos de um jeito mais interessante**.

> Se não existe desafio, ninguém continua. Se não existe tensão, ninguém se importa. Se não existe transformação, ninguém lembra.

### Os 5 passos rápidos (todo roteiro)
| Passo | Pergunta | No canal |
| --- | --- | --- |
| **1. Gancho** | Qual pergunta, dor ou curiosidade faz a pessoa querer ficar? | PROMESSA + GANCHO (até 20 s) |
| **2. Contexto** | O que a pessoa precisa saber para entrar na história sem se perder? | Bloco I, curto. Só o necessário |
| **3. Tensão** | O que está em jogo? O que pode dar errado? | Conflito escalando a cada bloco; altos e baixos (seção F) |
| **4. Progressão** | O vídeo leva do ponto A ao ponto B **sem enrolação**? | Cada bloco avança a história. Se um bloco pode sair sem fazer falta, sai |
| **5. Transformação** | A pessoa sai diferente do que entrou? | "Você nunca mais vai ver ______ do mesmo jeito" |

### A jornada do herói (para episódios com personagem)
Quando o vídeo tem um personagem real (Carnarvon, Enoque, um explorador), os 12 passos dão o esqueleto. Não precisa usar todos; os que estão em **negrito** não podem faltar.

| # | Passo | Exemplo (faraó) |
| --- | --- | --- |
| 1 | **Vida comum** | Lorde rico e doente, procurando a descoberta do século |
| 2 | **O chamado** | Carter acha um degrau embaixo da areia |
| 3 | Recusa / resistência | O dinheiro estava acabando |
| 4 | Ajuda / mentor | Carter, o especialista |
| 5 | **Primeiro desafio (a travessia)** | Abrir a porta lacrada: "coisas maravilhosas" |
| 6 | Testes, aliados, inimigos | Os jornais, o The Times, Conan Doyle |
| 7 | Aproximação do maior desafio | A câmara do faraó é aberta |
| 8 | **A crise** | A navalha, a febre, a morte |
| 9 | Recompensa / luz no fim do túnel | A pergunta: de onde veio a maldição? |
| 10 | Caminho de volta | A investigação: a frase nunca foi encontrada |
| 11 | **Ressurreição** | A maldição verdadeira (Khentika) e o fungo |
| 12 | **Retorno com prova da transformação** | "Estava no ar." O público sai vendo a lenda de outro jeito |

### Fechamento circular
**O final volta à imagem ou à frase da abertura**, agora com outro sentido (como o GTA V no começo e no fim do vídeo de referência). No faraó: a máscara abre e fecha o vídeo; "estava no ar" é prometido no gancho e respondido no fim. Isso dá sensação de história completa.

### A música entra junto com o roteiro
Antes de escrever, definir o **clima de cada bloco** (calmo, tensão, susto, revelação, silêncio). O mapa de tensão da trilha própria nasce do roteiro, e não depois da edição. A música aguça o sentimento que a cena já tem.

### Like e inscrição com motivo
O pedido funciona melhor ligado a uma promessa concreta: "o próximo é sobre ______, e você pode perder se não estiver inscrito". Nunca um pedido solto.

---

## Esqueleto de roteiro (copiar para cada episódio)

```
FICHA: personagem / conflito / clímax / resolução / transformação / tema / ponto de identificação (seção J)

### [00:00 – 00:05] PROMESSA
(cena = thumb, funciona sem som)  Frase 1 = título.

### [00:05 – 00:20] GANCHO
Contexto. O que está em jogo. Lacuna. Esforço (número real). "E não é só isso…"

### [00:20 – ~01:30] I. <PONTO 1>  (ciclo curto, revelação leve)
ALTA (animação/imagem) → BAIXA → GANCHO para o II

### II. <PONTO 2>  ... III. <PONTO 3>  ... (escalando; algo novo a cada ~3 min)
(chamada de like perto de 2:00)

### [últimos 20%] <O LADO OBSCURO>

### FECHAMENTO
Recompensa (responde a lacuna) → imagem forte → pergunta → gancho do próximo.
```

## Checklist antes de gravar o áudio

- [ ] A ideia é interessante, original e forte?
- [ ] Ficha da história preenchida: personagem com motivação, conflito, clímax, resolução, transformação e tema?
- [ ] O conflito aparece no gancho, e o público sai com a frase "você nunca mais vai ver ______ do mesmo jeito"?
- [ ] O fechamento acrescenta uma página ao arquivo e aponta a próxima?
- [ ] A introdução liga o tema a algo que a maioria do público já viveu ou ouviu?
- [ ] Os 5 passos estão lá (gancho, contexto, tensão, progressão, transformação) e nenhum bloco é só "sequência de fatos"?
- [ ] O final volta à imagem ou à frase da abertura (fechamento circular)?
- [ ] Título com até 50 caracteres e esboço da thumb prontos?
- [ ] Cena 1 = thumb, e os 5 primeiros segundos funcionam sem som?
- [ ] Gancho com contexto, recompensa, lacuna, esforço e "tem mais", em até 20 s?
- [ ] Cada bloco termina puxando o próximo, e as revelações crescem até o fim?
- [ ] Algo novo a cada ~3 min (motivo recorrente, curta, virada)?
- [ ] Frases de impacto viraram **cenas para animar** (e não texto na tela)?
- [ ] O final responde a lacuna e termina em alta?
- [ ] Todo número de "esforço" é verdadeiro?
- [ ] Qual é **a 1 melhoria** deste vídeo?

---

## Registro de retenção e melhorias (preencher 48 h e 7 dias após cada vídeo)

| Vídeo | Retenção média | Aos 30 s | Com legenda / dublado | Pontos de queda (tempo → motivo) | Melhoria testada | O que mudar no próximo |
| --- | --- | --- | --- | --- | --- | --- |
| O Favorzinho | | | | | Primeiro vídeo | |
| Até a luz de antigamente era diferente | 31,2% (2:19 de 7:27) | | Legenda PT 18,2% · EN 17,4% | | Clipes + música do Suno | Tema de "curiosidade geral" atraiu público de autoajuda (sugerido ao lado de Maquiavel): clique alto, retenção baixa. CTR 1,7% |
| Adão tinha poderes? | 33,5% (2:14 de 6:43) | 68% (acima da média) | | 0:48–1:00 → frase longa de história (Livro dos Jubileus, data); 1:30–2:00 → sequência de citações do Talmude; 4:19 → SOBE no "lado obscuro" (gente pulando para lá); 6:08 → cai no aviso "nada disso está na Bíblia" depois da recompensa | Gancho de 20 s + selo | Fonte depois da revelação e curta; parte obscura prometida no gancho e mais cedo; terminar logo depois da recompensa. CTR 3,1% em 3,9 mil impressões; 797 views, 143 intencionais |
| Paralisia do sono | 50,1% (3:04 de 6:08) | | | | Curta animado + trilha própria + Short "3h07" | Short do mesmo tema: 1.146 views e 71,2% de retenção (o conteúdo mais visto do canal). Sugerido ao lado de terror/Amazônia, com CTR de 19–40% nesses vizinhos. CTR geral 2,8% (4.897 impr.) |
| Enoque | 68,9% (4:16 de 6:12) · 1 dia | | | | Animação no lugar de texto + transições com som + CTA falado | Melhor retenção do canal no 1º dia. Acompanhar se o alcance sobe (CTR 1,7% em 524 impr.) |
| A maldição do faraó era real? | ~35% (1:58 de 5:39) · 1,5 dia, só 9 espectadores | | 46% na TV | | Thumbs em estilo novo (A/B: "NÃO FOI O FARAÓ" × "MALDIÇÃO"), sem Short | **CTR 1,2% (0,7% nas recomendações) em 1,6 mil impressões**: o YouTube entregou, o clique não veio. Sugerido ao lado de vídeos sem relação (Argonautas, futebol americano); quem veio de Matinta Pereira e "Capitalismo explicado" viu tudo. Tema saturado + a imagem mais batida do tema (a máscara) = some no meio das outras. Lição: tema já muito contado só entra com ângulo novo no título e na thumb; voltar para a linha forte (Bíblia oculta) e testar "Brasil obscuro". **A/B final (18–27/out): "NÃO FOI O FARAÓ" 62,7% × "MALDIÇÃO" 37,3%** — a frase que contradiz ganhou da palavra solta (o YouTube não declarou vencedor, mas manteve a variante 1) |
| Esse Deus não existe (bezerro) | | | | | Fundo que muda com a tensão + trilha contínua + SFX + voz para TV | Poucas views: **o tema saiu do foco do canal** (fé e comportamento, não mistério antigo). Lição: a técnica nova fica; o tema volta para culturas antigas e o lado obscuro delas |
| O alemão que os tupinambás iam comer (Staden) | | | | | 1º da linha "culturas antigas"; voz Google (Umbriel); gravuras reais + IA + palitos | **CTR 0,3% em 590 impressões (3 dias)**, 75% vindo de sugeridos. A thumb em line-art não mostrou que era história real. Próximo: real primeiro, thumb com foto real marcante |
