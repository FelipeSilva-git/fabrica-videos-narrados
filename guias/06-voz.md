# 06 · Voz (Gemini TTS ou ElevenLabs)

Narração gerada com o **Google AI Studio (Gemini TTS)** por `motor/google_tts.py`. Voz e estilo de cada canal ficam no perfil.

## Chaves
- `export GEMINI_API_KEYS="chave1,chave2,chave3"` **ou** `export GEMINI_KEYS_FILE=/caminho/fora/do/repo/chaves.txt` (uma por linha).
- O script troca de chave sozinho quando a cota acaba. **Nunca** imprima, cole ou versione as chaves.

## Uso
```bash
python3 motor/google_tts.py --listar                         # vozes disponíveis
python3 motor/google_tts.py voz/parte1.txt 1.wav --voz Umbriel --estilo "$(cat voz/estilo.txt)"
ffmpeg -i 1.wav -c:a libmp3lame -b:a 192k 1.mp3
```
Vozes que funcionaram: **Umbriel** (masculina, grave, calma) com estilo **Empathetic**. Teste 2–3 vozes com o mesmo parágrafo e deixe a pessoa escolher; registre no perfil.

## A regra mais importante: separar estilo do texto
Se as instruções de estilo vão junto com o texto, **a voz lê as instruções em voz alta** (aconteceu). O script monta assim:
```
<notas do diretor: estilo, ritmo, emoção>

#### TRANSCRIPT
<o texto a ser falado>
```
`voz/estilo.txt` (formato que funcionou; o script põe o `#### TRANSCRIPT` depois):
```
# AUDIO PROFILE: <nome do narrador>
<quem é, em uma linha>

## THE SCENE
<onde e para quem ele está contando>

### DIRECTOR'S NOTES
Estilo: empático, caloroso, tom suave.
Sotaque: português do Brasil natural.
Ritmo: calmo e pausado. Pausa curta entre frases, longa entre parágrafos.
Leia somente o texto da transcrição.
```
Exemplo real: `exemplo/video-teste/episodio-menina-inca/voz/estilo.txt`.

## Preparar o texto (voz/parteN.txt)
- **Partes de 1,5 a 2 minutos** (6 a 8 por vídeo de 10 min). Parte curta = refazer barato.
- **Sem tags `<break>`:** no Gemini as pausas vêm dos **parágrafos** (linha em branco). Frase de impacto = parágrafo próprio.
- **Números por extenso** ("mil quatrocentos e oitenta"), siglas como se leem.
- Nomes estrangeiros: escreva como se pronuncia se a voz errar (e mantenha a grafia certa no roteiro e na legenda).
- O arquivo `narracao-<ep>.md` (para o alinhamento) tem os mesmos textos em `## Parte N`, com os trechos separados por `<break time="1.0s" />` — cada trecho vira uma cena do storyboard.

## Conferir cada parte
- **Duração por palavra ≈ 0,29–0,37 s.** Muito acima disso: leu algo a mais (instrução, título). Muito abaixo: pulou trecho.
- Ouça o começo e o fim de cada parte.
- Gere **a parte 1 primeiro** e mostre para aprovação antes do resto.

## Alternativa: ElevenLabs
```bash
export ELEVENLABS_API_KEY=...            # elevenlabs.io > Profile > API Keys
python3 motor/elevenlabs_tts.py --listar
python3 motor/elevenlabs_tts.py voz/parte1.txt 1.mp3 --voz <voice_id>
```
- Aqui as pausas **podem** ir no texto com `<break time="1.0s" />` (1,5 s depois de frase de impacto, 2–3 s antes de virada).
- Não há "notas do diretor": o estilo vem da voz escolhida e de `--estabilidade` (mais baixo = mais expressivo).
- Partes de até ~4.500 caracteres. Uso comercial exige plano pago.
