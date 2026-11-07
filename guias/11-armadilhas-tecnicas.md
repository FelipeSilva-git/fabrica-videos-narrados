# 11 · Armadilhas técnicas (já aconteceram)

| Problema | Solução |
| --- | --- |
| A voz leu as instruções de estilo | estilo como "notas do diretor" + `#### TRANSCRIPT` antes do texto (guia 06) |
| Imagem real virou line-art | use `documento:` (PNG RGBA pronto), não `imagem:` |
| `preto` + `texto` na mesma cena: o texto some | não combine os dois |
| Glifo faltando (ex.: "−" U+2212) aparece como quadrado | use caracteres ASCII ("-") nos rótulos |
| Rótulos de animação sobrepostos | rótulo grande só na fase dele |
| Gerador de imagem recusa o prompt | reescreva tirando o elemento sensível; mostre antes/depois do ato |
| Wikimedia devolve 429 ou arquivo vazio | espere e tente de novo; use miniatura padrão (1280 px); confira tamanho > 0 |
| Thumb: a parte escura parece um corte | máscara com borda esfumada (gradiente longo), não borda dura |
| Descrição passou de 5.000 caracteres | tire as URLs dos créditos |
| Render longo morre quando a máquina reinicia | render em partes; os arquivos prontos ficam; relance só as que faltam |
| `pkill -f padrão` / `ps | grep padrão` matou o próprio terminal | não use padrões que aparecem no próprio comando; guarde o PID |
| Loop "espera até o log ter X" nunca acaba com log vazio | sempre tenha um limite de tempo |
| Arquivo final enorme | o `montar.sh` reencoda com `-crf 21 -maxrate 7M` |
| Áudio e vídeo dessincronizados nas emendas | use os `off` do `tempos.json` (soma das durações reais das partes) |
| Arquivo grande para transferir | divida em pedaços, confira o md5 depois de juntar |
